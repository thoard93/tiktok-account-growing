"""
Scheduler Service
=================
Background scheduler for automated warmup and posting tasks.
"""

import time
from datetime import datetime, timedelta
from typing import Optional, List
from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.account import Account, AccountStatus, ScheduleConfig
from app.services.warmup_service import WarmupService
from app.services.posting_service import PostingService
from app.services.geelark_client import GeeLarkClient
from app.config import get_settings


class AutomationScheduler:
    """
    Background scheduler for running automated tasks.
    
    Handles:
    - Daily warmup sessions for accounts in warmup phase
    - Automatic video posting for active accounts  
    - Task status monitoring
    - Cleanup of completed tasks
    """
    
    def __init__(self, geelark_client: GeeLarkClient):
        """Initialize scheduler with GeeLark client."""
        self.settings = get_settings()
        self.geelark = geelark_client
        self.scheduler = BackgroundScheduler()
        self._running = False
        
        logger.info("AutomationScheduler initialized")
    
    def _get_db_session(self) -> Session:
        """Get a new database session."""
        return SessionLocal()
    
    def _get_schedule_config(self, db: Session = None) -> dict:
        """
        Get scheduling configuration from database.
        Returns enabled status, phone_ids, and other settings.
        """
        close_db = False
        if db is None:
            db = self._get_db_session()
            close_db = True
        
        try:
            config = db.query(ScheduleConfig).filter(ScheduleConfig.key == "main").first()
            if config:
                return {
                    "enabled": config.enabled,
                    "phone_ids": config.phone_ids or [],
                    "posts_per_phone": config.posts_per_phone,
                    "enable_warmup": config.enable_warmup,
                    "auto_delete": config.auto_delete
                }
            else:
                return {
                    "enabled": False,
                    "phone_ids": [],
                    "posts_per_phone": 3,
                    "enable_warmup": True,
                    "auto_delete": True
                }
        finally:
            if close_db:
                db.close()
    
    # ===========================
    # Warmup Jobs
    # ===========================
    
    def run_daily_warmup(self):
        """
        Run warmup for all accounts in warming_up status.
        Called once per day by scheduler.
        """
        logger.info("Starting daily warmup job...")
        
        db = self._get_db_session()
        try:
            warmup_service = WarmupService(db, self.geelark)
            results = warmup_service.run_batch_warmup()
            
            logger.info(
                f"Daily warmup complete: {results['success']} success, "
                f"{results['failed']} failed, {results['completed']} completed warmup"
            )
            
        except Exception as e:
            logger.error(f"Daily warmup job failed: {e}")
        finally:
            db.close()
    
    def check_warmup_progress(self):
        """
        Check warmup progress and advance accounts to next day.
        Called periodically to monitor warmup completion.
        """
        logger.debug("Checking warmup progress...")
        
        db = self._get_db_session()
        try:
            # Get accounts that ran warmup today
            today = datetime.utcnow().date()
            yesterday = today - timedelta(days=1)
            
            warming_accounts = db.query(Account).filter(
                Account.status == AccountStatus.WARMING_UP,
                Account.warmup_complete == False
            ).all()
            
            for account in warming_accounts:
                # Check if last activity was today
                if account.last_activity and account.last_activity.date() == today:
                    # Already ran warmup today, check if can advance
                    pass
                elif account.last_activity and account.last_activity.date() < yesterday:
                    # Missed a day - may need reset or notification
                    logger.warning(
                        f"Account {account.id} missed warmup day "
                        f"(last: {account.last_activity})"
                    )
                    
        except Exception as e:
            logger.error(f"Warmup progress check failed: {e}")
        finally:
            db.close()
    
    # ===========================
    # Posting Jobs
    # ===========================
    
    def run_auto_posting(self):
        """
        Auto-post videos to active accounts.
        Called by scheduler based on posting schedule.
        """
        logger.info("Starting auto-posting job...")
        
        db = self._get_db_session()
        try:
            posting_service = PostingService(db, self.geelark)
            results = posting_service.auto_assign_and_post(
                videos_per_account=1
            )
            
            logger.info(
                f"Auto-posting complete: {results['videos_posted']} videos "
                f"posted to {results['accounts_used']} accounts"
            )
            
        except Exception as e:
            logger.error(f"Auto-posting job failed: {e}")
        finally:
            db.close()
    
    def run_daily_video_generation(self):
        """
        Generate AI teamwork trend videos and post to scheduled phones.
        Full pipeline: Claude prompt → Nano Banana Pro → Grok Imagine → FFmpeg → GeeLark post.
        """
        logger.info("Starting daily video generation job...")
        
        # Check if scheduling is enabled in database
        config = self._get_schedule_config()
        if not config.get("enabled"):
            logger.info("Scheduling is DISABLED in database config - skipping video generation")
            return
        
        phone_ids = config.get("phone_ids", [])
        posts_per_phone = config.get("posts_per_phone", 3)
        auto_delete = config.get("auto_delete", True)
        
        if not phone_ids:
            logger.warning("No phones configured for scheduling - skipping video generation")
            return
        
        # Calculate videos needed: phones × posts per phone
        videos_needed = len(phone_ids) * posts_per_phone
        
        logger.info(f"Schedule config: {len(phone_ids)} phones × {posts_per_phone} posts = {videos_needed} videos needed")
        
        try:
            from app.services.video_generator import get_video_generator
            import requests
            import os
            
            generator = get_video_generator()
            
            # Generate required number of videos
            style_hints = ["nature", "beach", "city", "sunset", "mountains"][:videos_needed]
            results = generator.generate_batch(
                count=videos_needed,
                style_hints=style_hints,
                skip_overlay=False
            )
            
            successful = [r for r in results if r.success]
            failed = [r for r in results if not r.success]
            
            total_cost = sum(r.cost_usd for r in results)
            
            logger.info(
                f"Daily video generation complete: {len(successful)} success, "
                f"{len(failed)} failed, total cost: ${total_cost:.2f}"
            )
            
            # Auto-post to configured phones
            if successful and phone_ids:
                video_filenames = [os.path.basename(r.video_path) for r in successful if r.video_path]
                logger.info(f"Videos ready for posting: {video_filenames}")
                
                logger.info(f"Auto-posting {len(video_filenames)} videos to {len(phone_ids)} phones with auto start/stop...")
                
                # Use internal API call to post/batch endpoint (handles all the flow)
                api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
                try:
                    resp = requests.post(
                        f"{api_base}/api/videos/post/batch",
                        json={
                            "videos": video_filenames,
                            "phone_ids": phone_ids,
                            "caption": "",
                            "hashtags": "#teamwork #teamworktrend #teamworkchallenge #teamworkmakesthedream #letsgo",
                            "auto_start": True,
                            "auto_stop": True,
                            "auto_delete": auto_delete,
                            "distribute_mode": "round_robin"  # Multiple videos per phone for scheduler
                        },
                        timeout=30  # Quick timeout - job runs in background now
                    )
                    if resp.status_code == 200:
                        result = resp.json()
                        if result.get("job_id"):
                            logger.info(f"Auto-posting job started: job_id={result['job_id']} - runs in background")
                        else:
                            logger.warning(f"Unexpected response format: {result}")
                    else:
                        logger.error(f"Auto-posting failed: {resp.status_code} - {resp.text}")
                except Exception as e:
                    logger.error(f"Auto-posting request failed: {e}")
            
        except Exception as e:
            logger.error(f"Daily video generation failed: {e}")
    
    # ===========================
    # Task Monitoring Jobs
    # ===========================
    
    def check_pending_tasks(self):
        """
        Check status of pending GeeLark tasks and update activity logs.
        """
        logger.debug("Checking pending tasks...")
        
        db = self._get_db_session()
        try:
            from app.models.account import ActivityLog
            
            # Get recent pending tasks (last 24 hours)
            cutoff = datetime.utcnow() - timedelta(hours=24)
            
            pending_logs = db.query(ActivityLog).filter(
                ActivityLog.geelark_task_id.isnot(None),
                ActivityLog.success == True,  # Initial success (task created)
                ActivityLog.created_at >= cutoff
            ).limit(50).all()
            
            if not pending_logs:
                return
            
            # Query task status
            task_ids = [log.geelark_task_id for log in pending_logs if log.geelark_task_id]
            if not task_ids:
                return
            
            response = self.geelark.query_tasks(task_ids)
            
            if response.success and response.data:
                items = response.data.get("items", [])
                task_map = {t["id"]: t for t in items}
                
                for log in pending_logs:
                    if log.geelark_task_id in task_map:
                        task = task_map[log.geelark_task_id]
                        status = task.get("status")
                        
                        # Update if failed
                        if status == 4:  # Failed
                            log.success = False
                            log.error_message = task.get("failDesc", "Task failed")
                            
                            # Update account if it was a critical action
                            if log.action_type in ["warmup_session", "video_posted"]:
                                account = db.query(Account).filter(
                                    Account.id == log.account_id
                                ).first()
                                if account and "blocked" in log.error_message.lower():
                                    account.status = AccountStatus.BANNED
                
                db.commit()
                
        except Exception as e:
            logger.error(f"Task monitoring failed: {e}")
        finally:
            db.close()
    
    def retry_failed_tasks(self):
        """
        Automatically retry tasks that failed due to transient errors.
        """
        logger.debug("Checking for tasks to retry...")
        
        db = self._get_db_session()
        try:
            from app.models.account import ActivityLog
            
            # Get recent failed tasks (last 6 hours)
            cutoff = datetime.utcnow() - timedelta(hours=6)
            
            failed_logs = db.query(ActivityLog).filter(
                ActivityLog.geelark_task_id.isnot(None),
                ActivityLog.success == False,
                ActivityLog.created_at >= cutoff
            ).limit(20).all()
            
            # Retryable error patterns (transient issues)
            retryable_patterns = [
                "network", "timeout", "loading", "connection",
                "20100", "20108", "20124", "20133"
            ]
            
            tasks_to_retry = []
            for log in failed_logs:
                error = (log.error_message or "").lower()
                if any(p in error for p in retryable_patterns):
                    tasks_to_retry.append(log.geelark_task_id)
            
            if tasks_to_retry:
                response = self.geelark._make_request(
                    "/task/restart",
                    {"ids": tasks_to_retry}
                )
                
                if response.success:
                    logger.info(f"Retried {len(tasks_to_retry)} failed tasks")
                    
        except Exception as e:
            logger.error(f"Task retry failed: {e}")
        finally:
            db.close()
    
    # ===========================
    # Scheduler Control
    # ===========================
    
    def start(self):
        """Start the scheduler with configured jobs."""
        if self._running:
            logger.warning("Scheduler already running")
            return
        
        # Daily warmup - runs at 8 AM EST (13:00 UTC) - 1 hour before video gen
        self.scheduler.add_job(
            self.run_daily_warmup,
            CronTrigger(hour=13, minute=0),  # 8 AM EST = 13:00 UTC
            id="daily_warmup",
            replace_existing=True,
            max_instances=1
        )
        
        # Auto-posting - 10 AM, 1 PM, 5 PM EST = 15, 18, 22 UTC
        self.scheduler.add_job(
            self.run_auto_posting,
            CronTrigger(hour="15,18,22"),  # 10 AM, 1 PM, 5 PM EST
            id="auto_posting",
            replace_existing=True,
            max_instances=1
        )
        
        # Task monitoring - runs every 5 minutes
        self.scheduler.add_job(
            self.check_pending_tasks,
            IntervalTrigger(minutes=5),
            id="task_monitor",
            replace_existing=True,
            max_instances=1
        )
        
        # Task retry - runs every 30 minutes
        self.scheduler.add_job(
            self.retry_failed_tasks,
            IntervalTrigger(minutes=30),
            id="task_retry",
            replace_existing=True,
            max_instances=1
        )
        
        # Warmup progress check - runs every hour
        self.scheduler.add_job(
            self.check_warmup_progress,
            IntervalTrigger(hours=1),
            id="warmup_progress",
            replace_existing=True,
            max_instances=1
        )
        
        # Daily video generation - 9 AM EST = 14:00 UTC
        self.scheduler.add_job(
            self.run_daily_video_generation,
            CronTrigger(hour=14, minute=0),  # 9 AM EST = 14:00 UTC
            id="daily_video_generation",
            replace_existing=True,
            max_instances=1
        )
        
        self.scheduler.start()
        self._running = True
        logger.info("AutomationScheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        if not self._running:
            return
        
        self.scheduler.shutdown(wait=True)
        self._running = False
        logger.info("AutomationScheduler stopped")
    
    def get_jobs(self) -> List[dict]:
        """Get list of scheduled jobs."""
        return [
            {
                "id": job.id,
                "next_run": str(job.next_run_time),
                "trigger": str(job.trigger)
            }
            for job in self.scheduler.get_jobs()
        ]
    
    def run_job_now(self, job_id: str) -> bool:
        """Manually trigger a job to run immediately."""
        job = self.scheduler.get_job(job_id)
        if job:
            job.modify(next_run_time=datetime.utcnow())
            return True
        return False


# Singleton instance
_scheduler_instance: Optional[AutomationScheduler] = None


def get_scheduler(geelark_client: GeeLarkClient) -> AutomationScheduler:
    """Get or create scheduler singleton."""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = AutomationScheduler(geelark_client)
    return _scheduler_instance
