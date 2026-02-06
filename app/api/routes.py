"""
API Routes
==========
FastAPI endpoints for account management, automation, and GeeLark integration.
"""

import os
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, BackgroundTasks
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.config import get_settings
from app.models.account import Account, Proxy, Video, ActivityLog, AccountStatus, ScheduleConfig
from app.services.geelark_client import GeeLarkClient
from app.services.account_manager import AccountManager
from app.services.warmup_service import WarmupService
from app.services.posting_service import PostingService
from app.api.schemas import (
    AccountCreate, AccountBatchCreate, AccountResponse, AccountListResponse,
    AccountUpdate, ProxyCreate, ProxyBulkCreate, ProxyResponse,
    VideoResponse, VideoListResponse,
    WarmupStart, WarmupSession, PostVideoRequest, BatchPostRequest,
    ActivityLogResponse, ActivityLogListResponse,
    HealthResponse, DashboardStats,
    PhoneCreateRequest, PhoneStartRequest,
    TaskQueryRequest, TaskCancelRequest, TaskRetryRequest,
    GeeLarkTaskResponse, GeeLarkTaskListResponse,
    FullSetupRequest, FullSetupResponse, CredentialResponse
)

router = APIRouter()
settings = get_settings()


# ===========================
# Dependencies
# ===========================

def get_geelark_client() -> GeeLarkClient:
    """Get configured GeeLark client."""
    creds = settings.get_geelark_credentials()
    
    if creds["method"] == "TOKEN":
        return GeeLarkClient(
            base_url=settings.geelark_api_base_url,
            auth_method="TOKEN",
            app_token=creds["token"]
        )
    else:
        return GeeLarkClient(
            base_url=settings.geelark_api_base_url,
            auth_method="KEY",
            app_id=creds["app_id"],
            api_key=creds["api_key"]
        )


def get_account_manager(
    db: Session = Depends(get_db),
    geelark: GeeLarkClient = Depends(get_geelark_client)
) -> AccountManager:
    return AccountManager(db, geelark)


def get_warmup_service(
    db: Session = Depends(get_db),
    geelark: GeeLarkClient = Depends(get_geelark_client)
) -> WarmupService:
    return WarmupService(db, geelark)


def get_posting_service(
    db: Session = Depends(get_db),
    geelark: GeeLarkClient = Depends(get_geelark_client)
) -> PostingService:
    return PostingService(db, geelark)


# ===========================
# Health & Status
# ===========================

@router.get("/health", response_model=HealthResponse, tags=["Status"])
async def health_check(
    db: Session = Depends(get_db),
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Check system health and connectivity."""
    # Test GeeLark connection
    geelark_ok = geelark.test_connection()
    
    # Get account counts
    total = db.query(Account).count()
    warming = db.query(Account).filter(Account.status == AccountStatus.WARMING_UP).count()
    active = db.query(Account).filter(Account.status == AccountStatus.ACTIVE).count()
    
    return HealthResponse(
        status="healthy" if geelark_ok else "degraded",
        geelark_connected=geelark_ok,
        database_connected=True,
        accounts_total=total,
        accounts_warming=warming,
        accounts_active=active,
        timestamp=datetime.utcnow()
    )


@router.get("/dashboard/stats", response_model=DashboardStats, tags=["Status"])
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    from datetime import timedelta
    
    today = datetime.utcnow().date()
    
    return DashboardStats(
        total_accounts=db.query(Account).count(),
        warming_up=db.query(Account).filter(Account.status == AccountStatus.WARMING_UP).count(),
        active=db.query(Account).filter(Account.status == AccountStatus.ACTIVE).count(),
        posting=db.query(Account).filter(Account.status == AccountStatus.POSTING).count(),
        paused=db.query(Account).filter(Account.status == AccountStatus.PAUSED).count(),
        banned=db.query(Account).filter(Account.status == AccountStatus.BANNED).count(),
        total_proxies=db.query(Proxy).count(),
        available_proxies=db.query(Proxy).filter(Proxy.is_assigned == False, Proxy.is_active == True).count(),
        total_videos=db.query(Video).count(),
        unposted_videos=db.query(Video).filter(Video.is_posted == False).count(),
        recent_posts=db.query(Video).filter(Video.is_posted == True).count(),
        tasks_today=db.query(ActivityLog).filter(
            ActivityLog.created_at >= datetime.combine(today, datetime.min.time())
        ).count()
    )


# ===========================
# Proxy Management
# ===========================

@router.get("/proxies", response_model=List[ProxyResponse], tags=["Proxies"])
async def list_proxies(
    db: Session = Depends(get_db),
    assigned: Optional[bool] = None,
    limit: int = Query(100, le=500)
):
    """List all proxies."""
    query = db.query(Proxy)
    if assigned is not None:
        query = query.filter(Proxy.is_assigned == assigned)
    return query.limit(limit).all()


@router.post("/proxies", response_model=ProxyResponse, tags=["Proxies"])
async def create_proxy(proxy: ProxyCreate, db: Session = Depends(get_db)):
    """Create a single proxy."""
    db_proxy = Proxy(**proxy.model_dump())
    db.add(db_proxy)
    db.commit()
    db.refresh(db_proxy)
    return db_proxy


@router.post("/proxies/bulk", response_model=List[ProxyResponse], tags=["Proxies"])
async def bulk_create_proxies(
    data: ProxyBulkCreate,
    manager: AccountManager = Depends(get_account_manager)
):
    """Bulk import proxies from text format (host:port:user:pass per line)."""
    lines = [line.strip() for line in data.proxy_list.split("\n") if line.strip()]
    proxies = manager.add_proxies_from_list(lines, data.protocol)
    return proxies


@router.delete("/proxies/{proxy_id}", tags=["Proxies"])
async def delete_proxy(proxy_id: int, db: Session = Depends(get_db)):
    """Delete a proxy."""
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")
    if proxy.is_assigned:
        raise HTTPException(status_code=400, detail="Cannot delete assigned proxy")
    
    db.delete(proxy)
    db.commit()
    return {"message": "Proxy deleted"}


# ===========================
# Account Management
# ===========================

@router.get("/accounts", response_model=AccountListResponse, tags=["Accounts"])
async def list_accounts(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0
):
    """List all accounts with optional filtering."""
    query = db.query(Account)
    if status:
        try:
            status_enum = AccountStatus(status)
            query = query.filter(Account.status == status_enum)
        except ValueError:
            pass
    
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    return AccountListResponse(total=total, items=items)


@router.post("/accounts", response_model=AccountResponse, tags=["Accounts"])
async def create_account(
    data: AccountCreate,
    manager: AccountManager = Depends(get_account_manager)
):
    """Create a single account with GeeLark cloud phone."""
    proxy = None
    if data.proxy_id:
        proxy = manager.db.query(Proxy).filter(Proxy.id == data.proxy_id).first()
    
    account = manager.create_single_account(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password=data.password,
        proxy=proxy
    )
    
    if not account:
        raise HTTPException(status_code=500, detail="Failed to create account")
    
    return account


@router.post("/accounts/batch", response_model=List[AccountResponse], tags=["Accounts"])
async def batch_create_accounts(
    data: AccountBatchCreate,
    manager: AccountManager = Depends(get_account_manager)
):
    """Create multiple accounts in batch."""
    accounts = manager.batch_create_accounts(
        count=data.count,
        credentials=data.credentials,
        name_prefix=data.name_prefix
    )
    return accounts


@router.get("/accounts/{account_id}", response_model=AccountResponse, tags=["Accounts"])
async def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get account details."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/accounts/{account_id}", response_model=AccountResponse, tags=["Accounts"])
async def update_account(
    account_id: int,
    data: AccountUpdate,
    db: Session = Depends(get_db)
):
    """Update account details."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(account, key, value)
    
    db.commit()
    db.refresh(account)
    return account


@router.post("/accounts/{account_id}/start", tags=["Accounts"])
async def start_account(
    account_id: int,
    manager: AccountManager = Depends(get_account_manager)
):
    """Start the GeeLark cloud phone for an account."""
    if manager.start_account(account_id):
        return {"message": "Account started"}
    raise HTTPException(status_code=500, detail="Failed to start account")


@router.post("/accounts/{account_id}/stop", tags=["Accounts"])
async def stop_account(
    account_id: int,
    manager: AccountManager = Depends(get_account_manager)
):
    """Stop the GeeLark cloud phone."""
    if manager.stop_account(account_id):
        return {"message": "Account stopped"}
    raise HTTPException(status_code=500, detail="Failed to stop account")


@router.post("/accounts/{account_id}/pause", tags=["Accounts"])
async def pause_account(
    account_id: int,
    manager: AccountManager = Depends(get_account_manager)
):
    """Pause automation for an account."""
    if manager.pause_account(account_id):
        return {"message": "Account paused"}
    raise HTTPException(status_code=500, detail="Failed to pause account")


@router.post("/accounts/{account_id}/resume", tags=["Accounts"])
async def resume_account(
    account_id: int,
    manager: AccountManager = Depends(get_account_manager)
):
    """Resume automation for an account."""
    if manager.resume_account(account_id):
        return {"message": "Account resumed"}
    raise HTTPException(status_code=500, detail="Failed to resume account")


@router.post("/accounts/{account_id}/install-tiktok", tags=["Accounts"])
async def install_tiktok(
    account_id: int,
    manager: AccountManager = Depends(get_account_manager)
):
    """Install TikTok on the account's cloud phone."""
    if manager.install_tiktok(account_id):
        return {"message": "TikTok installation started"}
    raise HTTPException(status_code=500, detail="Failed to install TikTok")


@router.post("/accounts/{account_id}/mark-banned", tags=["Accounts"])
async def mark_account_banned(
    account_id: int,
    reason: str = "",
    manager: AccountManager = Depends(get_account_manager)
):
    """Mark an account as banned."""
    if manager.mark_banned(account_id, reason):
        return {"message": "Account marked as banned"}
    raise HTTPException(status_code=404, detail="Account not found")


@router.delete("/accounts/{account_id}", tags=["Accounts"])
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """Delete an account from the database."""
    try:
        from app.models.account import Account, ActivityLog
        
        # First delete related activity logs
        db.query(ActivityLog).filter(ActivityLog.account_id == account_id).delete()
        
        # Then delete the account
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        db.delete(account)
        db.commit()
        return {"message": f"Account {account_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete: {str(e)}")


@router.post("/accounts/full-setup", response_model=FullSetupResponse, tags=["Accounts"])
async def full_automation_setup(
    data: FullSetupRequest,
    manager: AccountManager = Depends(get_account_manager)
):
    """
    🚀 Zero-touch automation: Proxy → Phone → TikTok → Account → Warmup.
    
    Provide a proxy string and the system will:
    1. Create an Android 15 cloud phone with the proxy
    2. Install TikTok
    3. Create a TikTok account with natural credentials
    4. Store credentials securely
    5. Start the warmup process
    
    If username is taken, retries with new credentials (up to max_retries times).
    """
    result = manager.full_automation_setup(
        proxy_string=data.proxy_string,
        name_prefix=data.name_prefix,
        max_username_retries=data.max_retries
    )
    
    return FullSetupResponse(**result)


@router.post("/accounts/full-setup-async", tags=["Accounts"])
async def full_automation_setup_async(
    data: FullSetupRequest,
    background_tasks: BackgroundTasks
):
    """
    🚀 ASYNC Zero-touch automation - Returns immediately with task_id.
    
    Use GET /tasks/{task_id} to poll for progress.
    
    This endpoint returns instantly and runs the full setup in the background:
    1. Create an Android 15 cloud phone with the proxy
    2. Install TikTok
    3. Create a TikTok account with natural credentials
    4. Store credentials securely
    5. Start the warmup process
    """
    from app.services.task_tracker import create_task
    
    # Create task immediately - this is synchronous and fast
    task_id = create_task("magic_setup", {
        "proxy_string": data.proxy_string[:50] + "..." if len(data.proxy_string) > 50 else data.proxy_string,
        "name_prefix": data.name_prefix
    })
    
    # Run in background - don't pass db/geelark, create fresh inside
    background_tasks.add_task(
        run_magic_setup_background,
        task_id=task_id,
        proxy_string=data.proxy_string,
        name_prefix=data.name_prefix,
        max_retries=data.max_retries
    )
    
    # Return immediately with task_id
    return {
        "task_id": task_id,
        "status": "started",
        "message": "Magic Setup launched! Poll /tasks/{task_id} for progress."
    }


def run_magic_setup_background(
    task_id: str,
    proxy_string: str,
    name_prefix: str,
    max_retries: int
):
    """Background worker for Magic Setup - creates its own session/client."""
    from app.services.task_tracker import update_task, TaskStatus
    from app.services.account_manager import AccountManager
    from app.database import SessionLocal
    
    # Create fresh database session and reuse the get_geelark_client helper
    db = SessionLocal()
    geelark = get_geelark_client()  # Use the properly configured client
    
    try:
        update_task(task_id, status=TaskStatus.RUNNING, progress=5, current_step="Initializing...")
        
        manager = AccountManager(db, geelark)
        
        def status_callback(step: str, progress: int):
            update_task(task_id, progress=progress, current_step=step, step_complete=step)
        
        result = manager.full_automation_setup(
            proxy_string=proxy_string,
            name_prefix=name_prefix,
            max_username_retries=max_retries,
            callback=status_callback
        )
        
        if result.get("success"):
            update_task(
                task_id,
                status=TaskStatus.COMPLETE,
                progress=100,
                current_step="Complete!",
                result=result
            )
        else:
            update_task(
                task_id,
                status=TaskStatus.FAILED,
                progress=100,
                current_step="Failed",
                error=result.get("error", "Unknown error"),
                result=result
            )
    
    except Exception as e:
        logger.error(f"Background Magic Setup failed: {e}")
        update_task(
            task_id,
            status=TaskStatus.FAILED,
            error=str(e),
            current_step="Error occurred"
        )
    
    finally:
        # Always close the session
        db.close()


@router.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task_status(task_id: str):
    """
    Get the status of a background task.
    
    Poll this endpoint every 3-5 seconds to get real-time progress.
    """
    from app.services.task_tracker import get_task
    
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.get("/tasks", tags=["Tasks"])
async def list_tasks(limit: int = 20):
    """Get recent background tasks."""
    from app.services.task_tracker import get_all_tasks
    
    return {"tasks": get_all_tasks(limit)}


@router.get("/credentials", response_model=List[CredentialResponse], tags=["Accounts"])
async def list_credentials():
    """
    Get all stored credentials from the secure vault.
    
    WARNING: Returns decrypted credentials. Use with caution.
    """
    from app.services.credential_vault import get_vault
    
    vault = get_vault()
    credentials = vault.get_all_credentials()
    
    return [
        CredentialResponse(
            account_id=c["account_id"],
            username=c["username"],
            email=c["email"],
            password=c["password"],
            phone_id=c.get("phone_id"),
            created_at=c.get("created_at", "")
        )
        for c in credentials
    ]


@router.get("/credentials/{account_id}", response_model=CredentialResponse, tags=["Accounts"])
async def get_credential(account_id: int):
    """Get credentials for a specific account."""
    from app.services.credential_vault import get_vault
    
    vault = get_vault()
    cred = vault.get_credential(account_id)
    
    if not cred:
        raise HTTPException(status_code=404, detail="Credentials not found")
    
    return CredentialResponse(
        account_id=cred["account_id"],
        username=cred["username"],
        email=cred["email"],
        password=cred["password"],
        phone_id=cred.get("phone_id"),
        created_at=cred.get("created_at", "")
    )


# ===========================
# Warmup Automation
# ===========================

@router.post("/warmup/start", tags=["Warmup"])
async def start_warmup(
    data: WarmupStart,
    warmup: WarmupService = Depends(get_warmup_service)
):
    """Initialize warmup for accounts."""
    results = {"started": 0, "failed": 0}
    for account_id in data.account_ids:
        if warmup.start_warmup(account_id):
            results["started"] += 1
        else:
            results["failed"] += 1
    return results


@router.post("/warmup/run-session", tags=["Warmup"])
async def run_warmup_session(
    data: WarmupSession,
    warmup: WarmupService = Depends(get_warmup_service)
):
    """Run warmup session for accounts."""
    return warmup.run_batch_warmup(data.account_ids)


@router.get("/warmup/pending", response_model=List[AccountResponse], tags=["Warmup"])
async def get_pending_warmup(db: Session = Depends(get_db)):
    """Get accounts pending warmup."""
    return db.query(Account).filter(
        Account.status == AccountStatus.WARMING_UP,
        Account.warmup_complete == False
    ).all()


# ===========================
# Video & Posting
# ===========================

@router.get("/videos", response_model=VideoListResponse, tags=["Videos"])
async def list_videos(
    db: Session = Depends(get_db),
    posted: Optional[bool] = None,
    limit: int = Query(50, le=200)
):
    """List all videos."""
    query = db.query(Video)
    if posted is not None:
        query = query.filter(Video.is_posted == posted)
    
    total = query.count()
    items = query.order_by(Video.created_at.desc()).limit(limit).all()
    
    return VideoListResponse(total=total, items=items)


@router.post("/videos/upload", response_model=VideoResponse, tags=["Videos"])
async def upload_video(
    file: UploadFile = File(...),
    caption: Optional[str] = None,
    hashtags: Optional[str] = None,
    posting: PostingService = Depends(get_posting_service)
):
    """Upload a video file."""
    content = await file.read()
    
    hashtag_list = None
    if hashtags:
        hashtag_list = [h.strip() for h in hashtags.split(",")]
    
    video = posting.add_video(
        filename=file.filename,
        file_content=content,
        caption=caption,
        hashtags=hashtag_list
    )
    
    if not video:
        raise HTTPException(status_code=500, detail="Failed to upload video")
    
    return video


@router.delete("/videos/legacy/{video_id}", tags=["Videos"])
async def delete_legacy_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Delete a legacy video from the database."""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Also delete the file if it exists
    if video.filepath:
        try:
            import os
            if os.path.exists(video.filepath):
                os.remove(video.filepath)
        except Exception:
            pass  # File might not exist
    
    db.delete(video)
    db.commit()
    return {"success": True, "message": f"Video {video_id} deleted"}


@router.post("/videos/{video_id}/post", tags=["Videos"])
async def post_video(
    video_id: int,
    data: PostVideoRequest,
    posting: PostingService = Depends(get_posting_service)
):
    """Post a video to TikTok."""
    success = posting.post_video(
        video_id=video_id,
        account_id=data.account_id,
        caption=data.caption,
        hashtags=data.hashtags
    )
    
    if success:
        return {"message": "Video posted successfully"}
    raise HTTPException(status_code=500, detail="Failed to post video")


@router.post("/posting/auto", tags=["Videos"])
async def auto_post_videos(
    data: BatchPostRequest,
    posting: PostingService = Depends(get_posting_service)
):
    """Automatically assign and post videos to accounts."""
    return posting.auto_assign_and_post(
        account_ids=data.account_ids,
        videos_per_account=data.videos_per_account
    )


# ===========================
# Activity Logs
# ===========================

@router.get("/logs", response_model=ActivityLogListResponse, tags=["Logs"])
async def get_activity_logs(
    db: Session = Depends(get_db),
    account_id: Optional[int] = None,
    action_type: Optional[str] = None,
    limit: int = Query(50, le=200)
):
    """Get activity logs."""
    query = db.query(ActivityLog)
    if account_id:
        query = query.filter(ActivityLog.account_id == account_id)
    if action_type:
        query = query.filter(ActivityLog.action_type == action_type)
    
    total = query.count()
    items = query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    
    return ActivityLogListResponse(total=total, items=items)


# ===========================
# GeeLark Direct API
# ===========================

@router.get("/geelark/phones", tags=["GeeLark"])
async def list_geelark_phones(
    geelark: GeeLarkClient = Depends(get_geelark_client),
    page: int = 1,
    page_size: int = 100  # Increased to get all phones at once (max 100)
):
    """List cloud phones directly from GeeLark."""
    response = geelark.list_phones(page=page, page_size=page_size)
    if response.success:
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/phones/create", tags=["GeeLark"])
async def create_geelark_phone(
    data: PhoneCreateRequest,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Create a cloud phone directly via GeeLark."""
    response = geelark.create_single_phone(
        name=data.name,
        proxy_string=data.proxy_string,
        mobile_type=data.mobile_type,
        group=data.group,
        tags=data.tags,
        region=data.region,
        language=data.language
    )
    if response.success:
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/phones/start", tags=["GeeLark"])
async def start_geelark_phones(
    data: PhoneStartRequest,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Start cloud phones via GeeLark."""
    response = geelark.start_phones(
        ids=data.ids,
        width=data.width,
        energy_saving_mode=data.energy_saving_mode
    )
    if response.success:
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/phones/stop", tags=["GeeLark"])
async def stop_geelark_phones(
    ids: List[str],
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Stop cloud phones via GeeLark."""
    response = geelark.stop_phones(ids)
    if response.success:
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/tasks/query", tags=["GeeLark"])
async def query_geelark_tasks(
    data: TaskQueryRequest,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Query task status from GeeLark. If task_ids provided, queries specific tasks. Otherwise returns task history."""
    # If specific task IDs provided, query those
    if data.task_ids:
        response = geelark.query_tasks(data.task_ids)
        if response.success:
            return {"items": response.data if isinstance(response.data, list) else [], "total": len(response.data or [])}
        raise HTTPException(status_code=500, detail=response.message)
    
    # Otherwise, get task history (last 7 days)
    history_data = {"size": data.page_size}
    response = geelark._make_request("/task/historyRecords", history_data)
    
    if response.success:
        items = response.data.get("list", []) if response.data else []
        
        # Filter by task_type if specified
        if data.task_type is not None:
            items = [t for t in items if t.get("taskType") == data.task_type]
        
        return {
            "items": items,
            "total": len(items),
            "page": data.page,
            "page_size": data.page_size
        }
    
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/tasks/cancel", tags=["GeeLark"])
async def cancel_geelark_tasks(
    data: TaskCancelRequest,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Cancel waiting/in-progress tasks."""
    response = geelark._make_request("/task/cancel", {"ids": data.task_ids})
    if response.success or response.code == 40006:  # Partial success
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/tasks/retry", tags=["GeeLark"])
async def retry_geelark_tasks(
    data: TaskRetryRequest,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Retry failed/cancelled tasks (up to 5 times)."""
    response = geelark._make_request("/task/restart", {"ids": data.task_ids})
    if response.success or response.code == 40006:  # Partial success
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.get("/geelark/tasks/history", tags=["GeeLark"])
async def get_task_history(
    geelark: GeeLarkClient = Depends(get_geelark_client),
    size: int = Query(50, le=100),
    last_id: Optional[str] = None
):
    """Get task history from last 7 days."""
    data = {"size": size}
    if last_id:
        data["lastId"] = last_id
    
    response = geelark._make_request("/task/historyRecords", data)
    if response.success:
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.get("/geelark/tasks/{task_id}/detail", tags=["GeeLark"])
async def get_task_detail(
    task_id: str,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """Get detailed task info with logs and screenshots."""
    response = geelark._make_request("/task/detail", {"id": task_id})
    if response.success:
        return response.data
    raise HTTPException(status_code=500, detail=response.message)


@router.post("/geelark/warmup/run", tags=["GeeLark"])
async def run_warmup_on_phone(
    data: dict,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """
    Run TikTok warmup on any GeeLark phone by ID.
    
    Args:
        phone_id: The GeeLark phone ID
        duration_minutes: Warmup duration (default 30)
        action: "browse video" or "search video" (default browse)
        keywords: List of search keywords for search mode
    """
    phone_id = data.get("phone_id")
    duration = data.get("duration_minutes", 30)
    action = data.get("action", "browse video")
    keywords = data.get("keywords")
    
    if not phone_id:
        raise HTTPException(status_code=400, detail="phone_id is required")
    
    enhanced = data.get("enhanced", False)
    enable_comments = data.get("enable_comments", True)
    enable_likes = data.get("enable_likes", True)
    
    if enhanced:
        # Use enhanced warmup with template chaining
        result = geelark.run_enhanced_warmup(
            phone_ids=[phone_id],
            duration_minutes=duration,
            keywords=keywords,
            enable_comments=enable_comments,
            enable_likes=enable_likes
        )
        return {
            "success": result.get("success", True),
            "message": "Enhanced warmup started with template chaining",
            "data": result
        }
    else:
        # Run standard warmup
        response = geelark.run_tiktok_warmup(
            phone_ids=[phone_id],
            duration_minutes=duration,
            action=action,
            keywords=keywords
        )
        return {
            "success": response.success,
            "message": response.message,
            "data": response.data
        }


@router.post("/geelark/warmup/enhanced", tags=["GeeLark"])
async def run_enhanced_warmup(
    data: dict,
    geelark: GeeLarkClient = Depends(get_geelark_client)
):
    """
    Run enhanced warmup with template chaining on multiple phones.
    Chains: AI Warmup → AI Comments → Random Like
    
    Args:
        phone_ids: List of GeeLark phone IDs
        duration_minutes: Warmup duration (default 30)
        keywords: List of search keywords for targeted browsing
        enable_comments: Enable AI comment generation (default True)
        enable_likes: Enable random likes (default True)
        like_probability: Percentage chance to like videos (default 30)
    """
    phone_ids = data.get("phone_ids", [])
    duration = data.get("duration_minutes", 30)
    keywords = data.get("keywords", ["teamwork", "motivation"])
    enable_comments = data.get("enable_comments", True)
    enable_likes = data.get("enable_likes", True)
    like_probability = data.get("like_probability", 30)
    
    if not phone_ids:
        raise HTTPException(status_code=400, detail="phone_ids is required")
    
    # Run enhanced warmup with template chaining
    result = geelark.run_enhanced_warmup(
        phone_ids=phone_ids,
        duration_minutes=duration,
        keywords=keywords,
        enable_comments=enable_comments,
        enable_likes=enable_likes,
        like_probability=like_probability
    )
    
    return {
        "success": result.get("success", True),
        "message": f"Enhanced warmup started on {len(phone_ids)} phone(s)",
        "main_task_id": result.get("warmup_task_id"),
        "chained_tasks": {
            "comments": result.get("comments_task_id"),
            "likes": result.get("likes_task_id")
        }
    }


# ===========================
# Video Generation Routes
# ===========================

# Simple in-memory job tracker for video generation
import threading
import uuid
_video_jobs = {}
_video_jobs_lock = threading.Lock()


def _run_video_generation_job(job_id: str, count: int, style: str, text_overlay: str, skip_overlay: bool):
    """Background worker for video generation."""
    from app.services.video_generator import get_video_generator
    
    try:
        with _video_jobs_lock:
            _video_jobs[job_id]["status"] = "running"
            _video_jobs[job_id]["message"] = f"Generating {count} video(s)..."
        
        logger.info(f"[Job {job_id}] Starting generation of {count} video(s), style={style}")
        generator = get_video_generator()
        
        if count == 1:
            logger.info(f"[Job {job_id}] Single video mode")
            result = generator.generate_teamwork_video(
                style_hint=style,
                text_overlay=text_overlay,
                skip_overlay=skip_overlay
            )
            results = [result]
        else:
            logger.info(f"[Job {job_id}] Batch mode: generating {count} videos with 10s delay between each")
            results = generator.generate_batch(
                count=count,
                style_hints=[style] if style else None,
                skip_overlay=skip_overlay
            )
        
        # Log results summary
        success_count = sum(1 for r in results if r.success)
        fail_count = sum(1 for r in results if not r.success)
        logger.info(f"[Job {job_id}] Generation complete: {success_count} success, {fail_count} failed out of {count} requested")
        
        for i, r in enumerate(results):
            if r.success:
                logger.info(f"[Job {job_id}] Video {i+1}: SUCCESS - {r.video_path}")
            else:
                logger.error(f"[Job {job_id}] Video {i+1}: FAILED - {r.error}")
        
        with _video_jobs_lock:
            _video_jobs[job_id]["status"] = "completed"
            _video_jobs[job_id]["message"] = f"Complete: {success_count}/{count} videos generated"
            _video_jobs[job_id]["results"] = [
                {
                    "success": r.success,
                    "video_path": r.video_path,
                    "text_overlay": r.text_overlay,
                    "cost_usd": r.cost_usd,
                    "error": r.error
                }
                for r in results
            ]
            _video_jobs[job_id]["total_cost_usd"] = sum(r.cost_usd for r in results)
            _video_jobs[job_id]["successful"] = success_count
            _video_jobs[job_id]["failed"] = fail_count
            
    except Exception as e:
        logger.error(f"Video generation job {job_id} failed: {e}")
        with _video_jobs_lock:
            _video_jobs[job_id]["status"] = "failed"
            _video_jobs[job_id]["message"] = str(e)


@router.post("/videos/generate")
async def generate_teamwork_video(
    data: dict,
    background_tasks: BackgroundTasks
):
    """
    Start video generation job (returns immediately).
    
    Pipeline: Claude prompt → Nano Banana Pro image → Grok video → FFmpeg overlay
    
    Returns a job_id to poll with /videos/job/{job_id}
    """
    style = data.get("style", None)
    text_overlay = data.get("text_overlay", None)
    skip_overlay = data.get("skip_overlay", False)
    
    job_id = str(uuid.uuid4())[:8]
    
    with _video_jobs_lock:
        _video_jobs[job_id] = {
            "status": "queued",
            "message": "Starting video generation...",
            "created_at": datetime.utcnow().isoformat(),
            "count": 1,
            "results": [],
            "total_cost_usd": 0,
            "successful": 0,
            "failed": 0
        }
    
    # Run in background thread (not blocking)
    thread = threading.Thread(
        target=_run_video_generation_job,
        args=(job_id, 1, style, text_overlay, skip_overlay),
        daemon=True
    )
    thread.start()
    
    return {
        "success": True,
        "job_id": job_id,
        "message": "Video generation started. Poll /videos/job/{job_id} for status."
    }


@router.post("/videos/batch")
async def generate_video_batch(data: dict):
    """
    Start batch video generation job (returns immediately).
    
    Returns a job_id to poll with /videos/job/{job_id}
    """
    count = min(data.get("count", 5), 20)
    styles = data.get("styles", None)
    skip_overlay = data.get("skip_overlay", False)
    
    style = styles[0] if styles and len(styles) > 0 else None
    job_id = str(uuid.uuid4())[:8]
    
    with _video_jobs_lock:
        _video_jobs[job_id] = {
            "status": "queued",
            "message": f"Starting batch generation of {count} videos...",
            "created_at": datetime.utcnow().isoformat(),
            "count": count,
            "results": [],
            "total_cost_usd": 0,
            "successful": 0,
            "failed": 0
        }
    
    thread = threading.Thread(
        target=_run_video_generation_job,
        args=(job_id, count, style, None, skip_overlay),
        daemon=True
    )
    thread.start()
    
    return {
        "success": True,
        "job_id": job_id,
        "message": f"Batch generation of {count} videos started. Poll /videos/job/{job_id} for status."
    }


@router.get("/videos/job/{job_id}")
async def get_video_job_status(job_id: str):
    """Get status of a video generation job."""
    with _video_jobs_lock:
        if job_id not in _video_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        return _video_jobs[job_id]


@router.get("/videos/list")
async def list_generated_videos():
    """List all generated videos in output directory."""
    from app.services.video_generator import get_video_generator
    from pathlib import Path
    
    generator = get_video_generator()
    video_dir = generator.output_dir
    
    videos = []
    if video_dir.exists():
        for video_file in video_dir.glob("teamwork_*.mp4"):
            stat = video_file.stat()
            videos.append({
                "filename": video_file.name,
                "path": str(video_file),
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })
    
    # Sort by newest first
    videos.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "count": len(videos),
        "videos": videos
    }


@router.get("/videos/caption")
async def get_random_caption():
    """Get random caption and hashtags for TikTok post."""
    from app.services.video_generator import VideoGenerator
    
    return {
        "caption": VideoGenerator.get_random_caption(),
        "hashtags": VideoGenerator.get_hashtags(),
        "full_description": VideoGenerator.get_full_description()
    }


@router.get("/videos/download/{filename}")
async def download_video(filename: str):
    """Stream a video file for download or preview."""
    from fastapi.responses import FileResponse
    from app.services.video_generator import get_video_generator
    
    generator = get_video_generator()
    video_path = generator.output_dir / filename
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=filename
    )


@router.delete("/videos/{filename}")
async def delete_video(filename: str):
    """Delete a generated video."""
    from app.services.video_generator import get_video_generator
    
    generator = get_video_generator()
    video_path = generator.output_dir / filename
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        video_path.unlink()
        return {"success": True, "message": f"Deleted {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/videos/upload")
async def upload_video_manual(
    file: UploadFile = File(...),
    caption: str = Form(""),
    hashtags: str = Form("")
):
    """
    Upload a video file manually.
    Saves to the generated_videos folder so it can be posted like AI-generated videos.
    """
    from app.services.video_generator import get_video_generator
    import shutil
    
    generator = get_video_generator()
    
    # Ensure output directory exists
    generator.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename to avoid conflicts
    timestamp = int(time.time())
    safe_filename = f"manual_{timestamp}_{file.filename}"
    video_path = generator.output_dir / safe_filename
    
    try:
        # Save the uploaded file
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Manual video uploaded: {safe_filename}")
        
        return {
            "success": True,
            "filename": safe_filename,
            "path": str(video_path),
            "caption": caption,
            "hashtags": hashtags,
            "message": "Video uploaded to generated videos folder"
        }
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===========================
# Video Posting Jobs (Background)
# ===========================

_posting_jobs = {}
_posting_jobs_lock = threading.Lock()


def _run_posting_job(job_id: str, video_filenames: list, phone_ids: list, caption: str, 
                     hashtags: str, auto_start: bool, auto_stop: bool, auto_delete: bool,
                     distribute_mode: str = "one_to_one"):
    """
    Background worker for video posting.
    
    distribute_mode:
      - 'one_to_one': video[0]→phone[0], video[1]→phone[1] (default for manual)
      - 'round_robin': video[i]→phone[i % len(phones)] (for scheduler, multiple posts per phone)
    """
    import time
    import requests as req
    from pathlib import Path
    from app.services.video_generator import get_video_generator
    from app.services.geelark_client import GeeLarkClient
    from app.core.config import settings
    
    logger.info(f"[PostJob {job_id}] Starting posting job for {len(video_filenames)} videos to {len(phone_ids)} phones")
    
    try:
        with _posting_jobs_lock:
            _posting_jobs[job_id]["status"] = "running"
            _posting_jobs[job_id]["message"] = "Initializing..."
        
        # Create fresh GeeLark client for background thread
        creds = settings.get_geelark_credentials()
        if creds.get("method") == "TOKEN":
            geelark = GeeLarkClient(
                base_url=settings.geelark_api_base_url,
                auth_method="TOKEN",
                app_token=creds.get("token")
            )
        else:
            geelark = GeeLarkClient(
                base_url=settings.geelark_api_base_url,
                auth_method="KEY",
                app_id=creds.get("app_id"),
                api_key=creds.get("api_key")
            )
        
        generator = get_video_generator()
        results = []
        phones_started = []
        
        # Step 0: Auto-start phones if needed
        if auto_start:
            with _posting_jobs_lock:
                _posting_jobs[job_id]["message"] = f"Starting {len(phone_ids)} phone(s)..."
            
            logger.info(f"[PostJob {job_id}] Auto-starting phones...")
            start_response = geelark.start_phones(phone_ids)
            if start_response.success:
                phones_started = phone_ids.copy()
                
                # Wait for phones to boot
                max_wait = 120
                wait_interval = 10
                waited = 0
                all_running = False
                
                while waited < max_wait and not all_running:
                    time.sleep(wait_interval)
                    waited += wait_interval
                    
                    with _posting_jobs_lock:
                        _posting_jobs[job_id]["message"] = f"Waiting for phones to boot... ({waited}s)"
                    
                    status_response = geelark.get_phone_status(phone_ids)
                    if status_response.success and status_response.data:
                        statuses = status_response.data
                        if isinstance(statuses, list):
                            all_running = all(s.get("status") == 0 or s.get("openStatus") == 0 for s in statuses)
                        elif isinstance(statuses, dict):
                            details = statuses.get("successDetails", [])
                            if details:
                                all_running = all(d.get("status") == 0 for d in details)
                    
                    logger.info(f"[PostJob {job_id}] Waited {waited}s, all_running={all_running}")
                
                if not all_running:
                    logger.warning(f"[PostJob {job_id}] Not all phones confirmed running, proceeding anyway")
        
        # Build full caption
        full_caption = f"{caption} {hashtags}".strip() if caption else hashtags
        
        with _posting_jobs_lock:
            _posting_jobs[job_id]["message"] = "Uploading and posting videos..."
        
        # Build video-phone pairs based on distribute_mode
        if distribute_mode == "round_robin":
            # Round-robin: each video goes to phone[i % len(phones)]
            # Allows multiple videos per phone for scheduler use case
            pairs = [(video_filenames[i], phone_ids[i % len(phone_ids)]) for i in range(len(video_filenames))]
            logger.info(f"[PostJob {job_id}] Round-robin distribution: {len(pairs)} postings across {len(phone_ids)} phones")
        else:
            # One-to-one: video[0]→phone[0], video[1]→phone[1] (default for manual)
            pairs = list(zip(video_filenames, phone_ids))
            logger.info(f"[PostJob {job_id}] One-to-one distribution: {len(pairs)} video-phone pairs")
        
        for video_filename, phone_id in pairs:
            video_path = generator.output_dir / video_filename
            
            if not video_path.exists():
                results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": "Video file not found"})
                continue
            
            # Get upload URL
            upload_response = geelark.get_upload_url(video_filename)
            if not upload_response.success:
                results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": f"Upload URL failed: {upload_response.message}"})
                continue
            
            upload_url = upload_response.data.get("uploadUrl") or upload_response.data.get("url")
            resource_url = upload_response.data.get("resourceUrl") or upload_response.data.get("accessUrl")
            
            if not upload_url:
                results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": "No upload URL returned"})
                continue
            
            # Upload to GeeLark OSS
            try:
                with open(video_path, "rb") as f:
                    upload_res = req.put(upload_url, data=f, timeout=120)
                    if upload_res.status_code not in [200, 201]:
                        results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": f"OSS upload failed: {upload_res.status_code}"})
                        continue
            except Exception as e:
                results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": f"Upload error: {str(e)}"})
                continue
            
            # Transfer to this specific phone
            transfer_response = geelark.upload_file_to_phone(
                phone_id=phone_id,
                resource_url=resource_url,
                destination_path="/sdcard/Download/"
            )
            
            if not transfer_response.success:
                results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": f"Transfer failed: {transfer_response.message}"})
                continue
            
            time.sleep(2)
            
            post_response = geelark.post_tiktok_video(
                phone_id=phone_id,
                video_url=resource_url,
                caption=full_caption
            )
            
            if post_response.success:
                task_id = post_response.data.get("taskId") or (post_response.data.get("taskIds") or [None])[0] if post_response.data else None
                results.append({"video": video_filename, "phone_id": phone_id, "success": True, "task_id": task_id})
                logger.info(f"[PostJob {job_id}] Posted {video_filename} → {phone_id[:8]}...")
            else:
                results.append({"video": video_filename, "phone_id": phone_id, "success": False, "error": f"Post failed: {post_response.message}"})
        
        successful = sum(1 for r in results if r.get("success"))
        failed = len(results) - successful
        
        # Auto-stop phones
        if auto_stop and phones_started:
            with _posting_jobs_lock:
                _posting_jobs[job_id]["message"] = "Stopping phones..."
            time.sleep(5)
            geelark.stop_phones(phones_started)
        
        # Auto-delete videos
        deleted_videos = []
        if auto_delete and successful > 0:
            for r in results:
                if r.get("success") and r.get("video"):
                    try:
                        video_path = generator.output_dir / r["video"]
                        if video_path.exists():
                            os.remove(video_path)
                            deleted_videos.append(r["video"])
                    except Exception:
                        pass
        
        with _posting_jobs_lock:
            _posting_jobs[job_id]["status"] = "completed"
            _posting_jobs[job_id]["message"] = f"Complete: {successful}/{len(results)} successful"
            _posting_jobs[job_id]["successful"] = successful
            _posting_jobs[job_id]["failed"] = failed
            _posting_jobs[job_id]["results"] = results
            _posting_jobs[job_id]["videos_deleted"] = len(deleted_videos)
        
        logger.info(f"[PostJob {job_id}] Complete: {successful} success, {failed} failed")
        
    except Exception as e:
        logger.error(f"[PostJob {job_id}] Failed: {e}")
        with _posting_jobs_lock:
            _posting_jobs[job_id]["status"] = "failed"
            _posting_jobs[job_id]["message"] = str(e)


@router.post("/videos/post/batch")
async def post_videos_to_tiktok(
    data: dict,
    background_tasks: BackgroundTasks
):
    """
    Start video posting job (returns immediately with job_id).
    Uses background task to prevent timeout.
    
    Poll /videos/post/job/{job_id} for status.
    """
    video_filenames = data.get("videos", [])
    phone_ids = data.get("phone_ids", [])
    caption = data.get("caption", "")
    hashtags = data.get("hashtags", "#teamwork #teamworktrend #teamworkchallenge")
    auto_start = data.get("auto_start", True)
    auto_stop = data.get("auto_stop", True)
    auto_delete = data.get("auto_delete", False)
    distribute_mode = data.get("distribute_mode", "one_to_one")  # 'one_to_one' or 'round_robin'
    
    if not video_filenames or not phone_ids:
        raise HTTPException(status_code=400, detail="Videos and phone_ids required")
    
    job_id = str(uuid.uuid4())[:8]
    
    with _posting_jobs_lock:
        _posting_jobs[job_id] = {
            "status": "queued",
            "message": "Starting posting job...",
            "created_at": datetime.utcnow().isoformat(),
            "videos": video_filenames,
            "phone_ids": phone_ids,
            "successful": 0,
            "failed": 0,
            "results": [],
            "videos_deleted": 0
        }
    
    # Start background task
    background_tasks.add_task(
        _run_posting_job,
        job_id, video_filenames, phone_ids, caption, hashtags, auto_start, auto_stop, auto_delete, distribute_mode
    )
    
    return {
        "success": True,
        "job_id": job_id,
        "message": f"Posting job started for {len(video_filenames)} video(s) to {len(phone_ids)} phone(s)",
        "poll_url": f"/api/videos/post/job/{job_id}"
    }


@router.get("/videos/post/job/{job_id}")
async def get_posting_job_status(job_id: str):
    """Get status of a posting job."""
    with _posting_jobs_lock:
        if job_id not in _posting_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        return _posting_jobs[job_id].copy()


@router.get("/videos/jobs")
async def list_all_jobs():
    """List all posting jobs for dashboard display."""
    with _posting_jobs_lock:
        jobs = []
        for job_id, job_data in _posting_jobs.items():
            jobs.append({
                "job_id": job_id,
                "status": job_data.get("status"),
                "message": job_data.get("message"),
                "created_at": job_data.get("created_at"),
                "videos": job_data.get("videos", []),
                "phone_ids": job_data.get("phone_ids", []),
                "successful": job_data.get("successful", 0),
                "failed": job_data.get("failed", 0)
            })
        # Sort by created_at descending
        jobs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return {"jobs": jobs[:20]}  # Return last 20 jobs


# ===========================
# Schedule Config Routes
# ===========================

@router.get("/schedule/config", tags=["Schedule"])
async def get_schedule_config(db: Session = Depends(get_db)):
    """
    Get the current scheduling configuration from database.
    Returns default values if no config exists.
    """
    config = db.query(ScheduleConfig).filter(ScheduleConfig.key == "main").first()
    
    if not config:
        # Return defaults
        return {
            "enabled": False,
            "phone_ids": [],
            "posts_per_phone": 3,
            "enable_warmup": True,
            "auto_delete": True,
            "updated_at": None
        }
    
    return {
        "enabled": config.enabled,
        "phone_ids": config.phone_ids or [],
        "posts_per_phone": config.posts_per_phone,
        "enable_warmup": config.enable_warmup,
        "auto_delete": config.auto_delete,
        "updated_at": config.updated_at.isoformat() if config.updated_at else None
    }


@router.post("/schedule/config", tags=["Schedule"])
async def save_schedule_config(data: dict, db: Session = Depends(get_db)):
    """
    Save scheduling configuration to database.
    Creates or updates the 'main' config entry.
    """
    config = db.query(ScheduleConfig).filter(ScheduleConfig.key == "main").first()
    
    if not config:
        # Create new config
        config = ScheduleConfig(key="main")
        db.add(config)
    
    # Update fields
    if "enabled" in data:
        config.enabled = data["enabled"]
    if "phone_ids" in data:
        config.phone_ids = data["phone_ids"]
    if "posts_per_phone" in data:
        config.posts_per_phone = data["posts_per_phone"]
    if "enable_warmup" in data:
        config.enable_warmup = data["enable_warmup"]
    if "auto_delete" in data:
        config.auto_delete = data["auto_delete"]
    
    config.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(config)
    
    logger.info(f"Schedule config updated: enabled={config.enabled}, phones={len(config.phone_ids or [])}")
    
    return {
        "success": True,
        "enabled": config.enabled,
        "phone_ids": config.phone_ids or [],
        "posts_per_phone": config.posts_per_phone,
        "enable_warmup": config.enable_warmup,
        "auto_delete": config.auto_delete,
        "updated_at": config.updated_at.isoformat() if config.updated_at else None
    }

