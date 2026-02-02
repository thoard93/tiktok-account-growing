"""
API Routes
==========
FastAPI endpoints for account management, automation, and GeeLark integration.
"""

import os
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, BackgroundTasks
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.config import get_settings
from app.models.account import Account, Proxy, Video, ActivityLog, AccountStatus
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
    """Query task status from GeeLark."""
    response = geelark.query_tasks(data.task_ids)
    if response.success:
        return response.data
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
    
    # Run warmup with specified mode
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
