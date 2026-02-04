"""
Posting Service
===============
Handles video upload and automated posting to TikTok.
"""

import os
import shutil
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pathlib import Path
from sqlalchemy.orm import Session
from loguru import logger

from app.models.account import Account, Video, AccountStatus, ActivityLog, Schedule, ScheduleType
from app.services.geelark_client import GeeLarkClient
from app.config import get_settings

settings = get_settings()


class PostingService:
    """
    Manages video uploads and TikTok posting automation.
    """
    
    def __init__(self, db: Session, geelark_client: GeeLarkClient):
        self.db = db
        self.geelark = geelark_client
        self.storage_path = Path(settings.video_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    # ===========================
    # Video Management
    # ===========================
    
    def add_video(
        self,
        filename: str,
        file_content: bytes,
        caption: Optional[str] = None,
        hashtags: Optional[List[str]] = None
    ) -> Optional[Video]:
        """
        Add a video to the library.
        
        Args:
            filename: Original filename
            file_content: Video file bytes
            caption: Video caption
            hashtags: List of hashtags
        """
        # Save to local storage
        safe_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        filepath = self.storage_path / safe_filename
        
        with open(filepath, "wb") as f:
            f.write(file_content)
        
        video = Video(
            filename=filename,
            filepath=str(filepath),
            file_size=len(file_content),
            caption=caption,
            hashtags=",".join(hashtags) if hashtags else None,
            is_uploaded_to_phone=False,
            is_posted=False
        )
        
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        
        logger.info(f"Added video {video.id}: {filename}")
        return video
    
    def get_videos(
        self,
        posted: Optional[bool] = None,
        account_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Video]:
        """Get videos with optional filtering."""
        query = self.db.query(Video)
        if posted is not None:
            query = query.filter(Video.is_posted == posted)
        if account_id:
            query = query.filter(Video.account_id == account_id)
        return query.order_by(Video.created_at.desc()).limit(limit).all()
    
    def get_unposted_videos(self, limit: int = 10) -> List[Video]:
        """Get videos that haven't been posted yet."""
        return self.db.query(Video).filter(
            Video.is_posted == False,
            Video.account_id == None  # Not assigned to an account yet
        ).limit(limit).all()
    
    def assign_video_to_account(self, video_id: int, account_id: int) -> bool:
        """Assign a video to an account for posting."""
        video = self.db.query(Video).filter(Video.id == video_id).first()
        account = self.db.query(Account).filter(Account.id == account_id).first()
        
        if not video or not account:
            return False
        
        video.account_id = account_id
        self.db.commit()
        return True
    
    # ===========================
    # GeeLark Video Upload
    # ===========================
    
    def upload_video_to_phone(self, video_id: int, account_id: int) -> bool:
        """
        Upload a video to the account's cloud phone.
        
        Steps:
        1. Get upload URL from GeeLark
        2. Upload file to URL
        3. Transfer to phone storage
        """
        video = self.db.query(Video).filter(Video.id == video_id).first()
        account = self.db.query(Account).filter(Account.id == account_id).first()
        
        if not video or not account or not account.geelark_profile_id:
            return False
        
        # Step 1: Get upload URL
        response = self.geelark.get_upload_url(
            filename=video.filename,
            content_type="video/mp4"
        )
        
        if not response.success:
            logger.error(f"Failed to get upload URL: {response.message}")
            return False
        
        upload_url = response.data.get("uploadUrl") or response.data.get("url")
        resource_url = response.data.get("resourceUrl") or response.data.get("accessUrl")
        
        # Step 2: Upload file to URL (if upload_url provided)
        if upload_url:
            import requests
            with open(video.filepath, "rb") as f:
                upload_response = requests.put(upload_url, data=f)
                if upload_response.status_code not in [200, 201]:
                    logger.error(f"Failed to upload file: {upload_response.status_code}")
                    return False
        
        # Step 3: Transfer to phone
        if resource_url:
            transfer_response = self.geelark.upload_file_to_phone(
                phone_id=account.geelark_profile_id,
                resource_url=resource_url,
                destination_path="/sdcard/DCIM/TikTok/"
            )
            
            if transfer_response.success:
                video.is_uploaded_to_phone = True
                video.geelark_resource_url = resource_url
                video.account_id = account_id
                self.db.commit()
                
                self._log_activity(account_id, "video_uploaded", {
                    "video_id": video_id,
                    "filename": video.filename
                })
                
                logger.info(f"Uploaded video {video_id} to account {account_id}")
                return True
        
        return False
    
    # ===========================
    # Posting Automation
    # ===========================
    
    def post_video(
        self,
        video_id: int,
        account_id: int,
        caption: Optional[str] = None,
        hashtags: Optional[List[str]] = None,
        auto_start: bool = True,
        auto_stop: bool = True
    ) -> bool:
        """
        Post a video to TikTok.
        
        Args:
            video_id: Video to post
            account_id: Account to post from
            caption: Override caption
            hashtags: Override hashtags
            auto_start: Auto-start phone before posting (default True)
            auto_stop: Auto-stop phone after posting (default True)
        """
        import time
        
        video = self.db.query(Video).filter(Video.id == video_id).first()
        account = self.db.query(Account).filter(Account.id == account_id).first()
        
        if not video or not account or not account.geelark_profile_id:
            logger.error(f"Invalid video/account or missing geelark_profile_id")
            return False
        
        phone_id = account.geelark_profile_id
        phone_started = False
        
        try:
            # Auto-start phone if needed
            if auto_start:
                logger.info(f"Auto-starting phone {phone_id} for posting...")
                start_response = self.geelark.start_phones([phone_id])
                if start_response.success:
                    phone_started = True
                    # Wait for phone to boot (poll every 10s for up to 2 min)
                    max_wait = 120
                    wait_interval = 10
                    waited = 0
                    phone_running = False
                    
                    while waited < max_wait and not phone_running:
                        time.sleep(wait_interval)
                        waited += wait_interval
                        status_response = self.geelark.get_phone_status([phone_id])
                        if status_response.success and status_response.data:
                            statuses = status_response.data
                            if isinstance(statuses, list) and len(statuses) > 0:
                                phone_running = statuses[0].get("status") == 0 or statuses[0].get("openStatus") == 0
                        logger.info(f"Waiting for phone boot: {waited}s, running={phone_running}")
                    
                    if not phone_running:
                        logger.warning("Phone not confirmed running, proceeding anyway...")
                else:
                    logger.warning(f"Failed to start phone: {start_response.message}")
            
            # Ensure video is uploaded to GeeLark OSS
            if not video.geelark_resource_url:
                if not self.upload_video_to_phone(video_id, account_id):
                    return False
                # Refresh video object
                self.db.refresh(video)
            
            # Prepare caption with hashtags
            final_caption = caption or video.caption or ""
            if hashtags:
                final_caption += " " + " ".join([f"#{tag}" for tag in hashtags])
            elif video.hashtags:
                final_caption += " " + " ".join([f"#{tag}" for tag in video.hashtags.split(",")])
            
            # Execute posting using resourceUrl directly
            response = self.geelark.post_tiktok_video(
                phone_id=phone_id,
                video_url=video.geelark_resource_url,  # Use OSS URL directly
                caption=final_caption
            )
            
            if response.success:
                video.is_posted = True
                video.posted_at = datetime.utcnow()
                account.posts_count += 1
                account.last_activity = datetime.utcnow()
                account.status = AccountStatus.POSTING
                self.db.commit()
                
                self._log_activity(account_id, "video_posted", {
                    "video_id": video_id,
                    "caption": final_caption[:100],
                    "task_id": response.data.get("taskId") or (response.data.get("taskIds") or [None])[0] if response.data else None
                })
                
                logger.info(f"Posted video {video_id} from account {account_id}")
                return True
            else:
                self._log_activity(
                    account_id, "video_posted",
                    {"video_id": video_id, "error": response.message},
                    success=False,
                    error=response.message
                )
                return False
                
        finally:
            # Auto-stop phone if we started it
            if auto_stop and phone_started:
                logger.info(f"Auto-stopping phone {phone_id} after posting...")
                time.sleep(5)  # Let task register
                self.geelark.stop_phones([phone_id])
    
    def schedule_post(
        self,
        video_id: int,
        account_id: int,
        post_time: datetime
    ) -> Optional[Schedule]:
        """Schedule a video to be posted at a specific time."""
        schedule = Schedule(
            account_id=account_id,
            schedule_type=ScheduleType.POST_VIDEO,
            run_at=post_time,
            repeat_daily=False,
            is_active=True,
            config={"video_id": video_id}
        )
        
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        
        return schedule
    
    def auto_assign_and_post(
        self,
        account_ids: Optional[List[int]] = None,
        videos_per_account: int = 1
    ) -> Dict:
        """
        Automatically assign and post videos to accounts.
        
        Args:
            account_ids: Specific accounts, or None for all active accounts
            videos_per_account: Number of videos to post per account
        """
        if account_ids:
            accounts = self.db.query(Account).filter(
                Account.id.in_(account_ids),
                Account.status.in_([AccountStatus.ACTIVE, AccountStatus.POSTING])
            ).all()
        else:
            accounts = self.db.query(Account).filter(
                Account.status.in_([AccountStatus.ACTIVE, AccountStatus.POSTING]),
                Account.warmup_complete == True
            ).all()
        
        unposted_videos = self.get_unposted_videos(limit=len(accounts) * videos_per_account)
        
        results = {
            "accounts_processed": 0,
            "videos_posted": 0,
            "failed": 0
        }
        
        video_index = 0
        for account in accounts:
            for _ in range(videos_per_account):
                if video_index >= len(unposted_videos):
                    break
                    
                video = unposted_videos[video_index]
                video_index += 1
                
                if self.post_video(video.id, account.id):
                    results["videos_posted"] += 1
                else:
                    results["failed"] += 1
                
                # Delay between posts
                import time
                import random
                delay = random.randint(
                    settings.min_delay_seconds * 2,
                    settings.max_delay_seconds * 2
                )
                time.sleep(delay)
            
            results["accounts_processed"] += 1
        
        logger.info(f"Auto post complete: {results}")
        return results
    
    # ===========================
    # Caption Generation (Placeholder)
    # ===========================
    
    def generate_caption(self, video_id: int, niche: str = "general") -> str:
        """
        Generate a caption for a video.
        
        TODO: Integrate with AI (GeeLark AI or external) for generation.
        """
        # Placeholder - returns template caption
        templates = {
            "general": "Check this out! 🔥 #fyp #viral #trending",
            "shop": "Shop this look! 🛍️ Link in bio #tiktokshop #musthave",
            "funny": "Wait for it... 😂 #funny #comedy #lol",
            "lifestyle": "Living my best life ✨ #lifestyle #aesthetic #vibes"
        }
        return templates.get(niche, templates["general"])
    
    # ===========================
    # Utility
    # ===========================
    
    def _log_activity(
        self,
        account_id: int,
        action_type: str,
        details: Dict,
        success: bool = True,
        error: Optional[str] = None
    ):
        """Log posting activity."""
        log = ActivityLog(
            account_id=account_id,
            action_type=action_type,
            action_details=details,
            success=success,
            error_message=error
        )
        self.db.add(log)
        self.db.commit()
