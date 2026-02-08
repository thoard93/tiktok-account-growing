"""
Scheduler Service v2.0
======================
Background scheduler for the automated daily pipeline.

Pipeline (all times EST):
  1. Warmup  — 8:00 AM  (configurable)
  2. Video Generation — 9:00 AM  (configurable)
  3. Video Posting — 10 AM, 1 PM, 5 PM  (configurable)

Uses per-account scheduling: each Account has schedule_enabled, schedule_warmup,
and schedule_posting flags. ScheduleConfig.enabled is the master switch.
"""

import time
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from loguru import logger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.account import Account, ScheduleConfig, PipelineLog, AccountStatus
from app.services.geelark_client import GeeLarkClient
from app.config import get_settings

# EST is UTC-5 (no DST handling — simple offset)
EST_OFFSET = 5


def est_to_utc(est_hour: int) -> int:
    """Convert EST hour to UTC hour."""
    return (est_hour + EST_OFFSET) % 24


class AutomationScheduler:
    """
    Background scheduler for the automated daily pipeline.
    
    Pipeline phases:
    1. Warmup: Start GeeLark phones, run TikTok browsing
    2. Video Generation: Generate AI teamwork videos
    3. Posting: Upload and post videos to scheduled accounts
    """
    
    def __init__(self, geelark_client: GeeLarkClient):
        self.settings = get_settings()
        self.geelark = geelark_client
        self.scheduler = BackgroundScheduler()
        self._running = False
        logger.info("AutomationScheduler v2.0 initialized")
    
    def _get_db(self) -> Session:
        """Get a new database session."""
        return SessionLocal()
    
    def _get_config(self, db: Session = None) -> dict:
        """Get global schedule config from database."""
        close = db is None
        if close:
            db = self._get_db()
        try:
            config = db.query(ScheduleConfig).filter(ScheduleConfig.key == "main").first()
            if config:
                return {
                    "enabled": config.enabled,
                    "posts_per_phone": config.posts_per_phone,
                    "enable_warmup": config.enable_warmup,
                    "auto_delete": config.auto_delete,
                    "warmup_hour_est": config.warmup_hour_est or 8,
                    "video_gen_hour_est": config.video_gen_hour_est or 9,
                    "posting_hours_est": config.posting_hours_est or "10,13,17",
                    # Legacy: also read phone_ids for backwards compat
                    "phone_ids": config.phone_ids or [],
                }
            return {
                "enabled": False,
                "posts_per_phone": 3,
                "enable_warmup": True,
                "auto_delete": True,
                "warmup_hour_est": 8,
                "video_gen_hour_est": 9,
                "posting_hours_est": "10,13,17",
                "phone_ids": [],
            }
        finally:
            if close:
                db.close()
    
    def _get_scheduled_accounts(self, db: Session, phase: str = "all") -> List[Account]:
        """Get accounts that are scheduled for the given phase."""
        query = db.query(Account).filter(Account.schedule_enabled == True)
        if phase == "warmup":
            query = query.filter(Account.schedule_warmup == True)
        elif phase == "posting":
            query = query.filter(Account.schedule_posting == True)
        return query.all()
    
    def _log_pipeline(self, db: Session, phase: str, status: str,
                      phone_id: str = None, account_name: str = None,
                      details: dict = None, error: str = None,
                      duration: float = None) -> PipelineLog:
        """Write a PipelineLog entry."""
        log = PipelineLog(
            pipeline_date=date.today(),
            phase=phase,
            phone_id=phone_id,
            account_name=account_name,
            status=status,
            details=details,
            error_message=error,
            duration_seconds=duration,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow() if status in ("completed", "failed", "skipped") else None,
        )
        db.add(log)
        db.commit()
        return log
    
    # =====================================================================
    # Phase 1: Daily Warmup
    # =====================================================================
    
    def run_daily_warmup(self):
        """
        Run warmup for all accounts with schedule_enabled + schedule_warmup.
        Each account's GeeLark phone is started, warmup flow is run, then stopped.
        """
        logger.info("=" * 50)
        logger.info("PIPELINE PHASE 1: Daily Warmup")
        logger.info("=" * 50)
        
        config = self._get_config()
        if not config["enabled"]:
            logger.info("Pipeline DISABLED — skipping warmup")
            return
        
        if not config["enable_warmup"]:
            logger.info("Warmup disabled in config — skipping")
            return
        
        db = self._get_db()
        try:
            accounts = self._get_scheduled_accounts(db, "warmup")
            if not accounts:
                logger.info("No accounts scheduled for warmup")
                self._log_pipeline(db, "warmup", "skipped",
                                   details={"reason": "no_accounts_scheduled"})
                return
            
            logger.info(f"Warming up {len(accounts)} accounts")
            self._log_pipeline(db, "warmup", "started",
                               details={"account_count": len(accounts)})
            
            success_count = 0
            fail_count = 0
            
            for account in accounts:
                phone_id = account.geelark_profile_id
                name = account.geelark_profile_name or f"Account #{account.id}"
                
                if not phone_id:
                    logger.warning(f"Skipping {name} — no GeeLark phone ID")
                    fail_count += 1
                    continue
                
                start_time = time.time()
                try:
                    logger.info(f"  → Warmup: {name} ({phone_id})")
                    
                    # Start the phone
                    start_resp = self.geelark.start_phones([phone_id])
                    if not start_resp.success:
                        raise Exception(f"Failed to start phone: {start_resp.message}")
                    
                    # Wait for phone boot
                    time.sleep(30)
                    
                    # Run warmup flow via GeeLark API directly
                    warmup_resp = self.geelark.run_tiktok_warmup(
                        phone_ids=[phone_id],
                        duration_minutes=20,
                        action="search video",
                        keywords=["teamwork trend", "teamwork challenge"]
                    )
                    if not warmup_resp.success:
                        raise Exception(f"Warmup task failed: {warmup_resp.message}")
                    
                    task_id = warmup_resp.data.get("taskId") if warmup_resp.data else None
                    logger.info(f"    Warmup task submitted: {task_id}")
                    
                    # Wait briefly then move on - warmup runs asynchronously
                    time.sleep(60)
                    
                    duration = time.time() - start_time
                    self._log_pipeline(db, "warmup", "completed",
                                       phone_id=phone_id, account_name=name,
                                       duration=duration)
                    success_count += 1
                    logger.info(f"  ✓ Warmup complete: {name} ({duration:.0f}s)")
                    
                except Exception as e:
                    duration = time.time() - start_time
                    self._log_pipeline(db, "warmup", "failed",
                                       phone_id=phone_id, account_name=name,
                                       error=str(e), duration=duration)
                    fail_count += 1
                    logger.error(f"  ✗ Warmup failed for {name}: {e}")
                
                finally:
                    # Always try to stop the phone after warmup
                    try:
                        self.geelark.stop_phones([phone_id])
                    except Exception:
                        pass
                    
                    # Small delay between accounts
                    time.sleep(5)
            
            logger.info(f"Warmup phase complete: {success_count} success, {fail_count} failed")
            
        except Exception as e:
            logger.error(f"Warmup phase crashed: {e}")
            self._log_pipeline(db, "warmup", "failed", error=str(e))
        finally:
            db.close()
    
    # =====================================================================
    # Phase 2: Daily Video Generation
    # =====================================================================
    
    def run_daily_video_generation(self):
        """
        Generate AI teamwork videos for all scheduled posting accounts.
        Videos per account = posts_per_phone from config.
        """
        logger.info("=" * 50)
        logger.info("PIPELINE PHASE 2: Video Generation")
        logger.info("=" * 50)
        
        config = self._get_config()
        if not config["enabled"]:
            logger.info("Pipeline DISABLED — skipping video generation")
            return
        
        db = self._get_db()
        try:
            accounts = self._get_scheduled_accounts(db, "posting")
            if not accounts:
                logger.info("No accounts scheduled for posting — skipping video gen")
                self._log_pipeline(db, "video_gen", "skipped",
                                   details={"reason": "no_accounts_scheduled"})
                return
            
            posts_per = config["posts_per_phone"]
            videos_needed = len(accounts) * posts_per
            
            logger.info(f"Generating {videos_needed} videos ({len(accounts)} accounts × {posts_per} each)")
            self._log_pipeline(db, "video_gen", "started",
                               details={"videos_needed": videos_needed,
                                        "account_count": len(accounts)})
            
            start_time = time.time()
            
            from app.services.video_generator import get_video_generator
            generator = get_video_generator()
            
            style_hints = ["nature", "beach", "city", "sunset", "mountains",
                          "forest", "ocean", "snow", "desert", "garden"]
            results = generator.generate_batch(
                count=videos_needed,
                style_hints=style_hints[:videos_needed],
                skip_overlay=False
            )
            
            successful = [r for r in results if r.success]
            failed = [r for r in results if not r.success]
            total_cost = sum(r.cost_usd for r in results)
            duration = time.time() - start_time
            
            self._log_pipeline(db, "video_gen", "completed",
                               details={
                                   "videos_generated": len(successful),
                                   "videos_failed": len(failed),
                                   "cost_usd": round(total_cost, 2),
                               },
                               duration=duration)
            
            logger.info(
                f"Video generation complete: {len(successful)} success, "
                f"{len(failed)} failed, ${total_cost:.2f} cost, {duration:.0f}s"
            )
            
        except Exception as e:
            logger.error(f"Video generation phase crashed: {e}")
            self._log_pipeline(db, "video_gen", "failed", error=str(e))
        finally:
            db.close()
    
    # =====================================================================
    # Phase 3: Auto-Posting
    # =====================================================================
    
    def run_auto_posting(self):
        """
        Post generated videos to all scheduled posting accounts.
        
        STAGGERED POSTING: Splits available videos evenly across posting time slots.
        e.g., with 3 videos and slots at 10, 1, 5 → posts 1 video per slot.
        Uses current UTC hour to determine which slot is firing.
        """
        logger.info("=" * 50)
        logger.info("PIPELINE PHASE 3: Auto-Posting (Staggered)")
        logger.info("=" * 50)
        
        config = self._get_config()
        if not config["enabled"]:
            logger.info("Pipeline DISABLED — skipping posting")
            return
        
        db = self._get_db()
        try:
            accounts = self._get_scheduled_accounts(db, "posting")
            if not accounts:
                logger.info("No accounts scheduled for posting")
                self._log_pipeline(db, "posting", "skipped",
                                   details={"reason": "no_accounts_scheduled"})
                return
            
            phone_ids = [a.geelark_profile_id for a in accounts if a.geelark_profile_id]
            if not phone_ids:
                logger.warning("Scheduled accounts have no phone IDs")
                return
            
            # Determine which time slot we're in (for staggered posting)
            posting_hours_str = config["posting_hours_est"]
            posting_hours = [int(h.strip()) for h in posting_hours_str.split(",")]
            num_slots = len(posting_hours)
            
            # Get current EST hour to match against slots
            from datetime import datetime, timezone, timedelta
            est = timezone(timedelta(hours=-5))
            current_est_hour = datetime.now(est).hour
            
            # Find which slot index we're closest to
            slot_index = 0
            for i, h in enumerate(posting_hours):
                if abs(current_est_hour - h) <= 1:  # Within 1 hour tolerance
                    slot_index = i
                    break
            
            logger.info(f"Posting slot {slot_index + 1}/{num_slots} (EST hour: {current_est_hour}, slots: {posting_hours})")
            
            self._log_pipeline(db, "posting", "started",
                               details={"phone_count": len(phone_ids), "slot": slot_index + 1, "total_slots": num_slots})
            
            start_time = time.time()
            
            import requests
            # Use Render external URL or fall back to localhost
            internal_base = os.getenv("RENDER_EXTERNAL_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")
            
            videos_resp = requests.get(f"{internal_base}/api/videos/list", timeout=10)
            if videos_resp.status_code != 200:
                raise Exception(f"Failed to get video list: {videos_resp.status_code}")
            
            videos_data = videos_resp.json()
            all_video_filenames = [v["filename"] for v in videos_data.get("videos", [])]
            
            if not all_video_filenames:
                logger.warning("No videos available for posting")
                self._log_pipeline(db, "posting", "skipped",
                                   details={"reason": "no_videos_available"})
                return
            
            # STAGGER: Calculate this slot's share of videos
            posts_per_phone = config["posts_per_phone"]
            total_posts_today = posts_per_phone * len(phone_ids)
            posts_per_slot = max(1, total_posts_today // num_slots)
            
            # Calculate which videos belong to this slot
            slot_start = slot_index * posts_per_slot * len(phone_ids)
            slot_end = slot_start + posts_per_slot * len(phone_ids)
            slot_videos = all_video_filenames[slot_start:slot_end]
            
            # If last slot, take any remaining videos too
            if slot_index == num_slots - 1:
                slot_videos = all_video_filenames[slot_start:]
            
            if not slot_videos:
                logger.info(f"Slot {slot_index + 1}: No videos left for this time slot")
                self._log_pipeline(db, "posting", "skipped",
                                   details={"reason": "no_videos_for_slot", "slot": slot_index + 1})
                return
            
            logger.info(f"Slot {slot_index + 1}: Posting {len(slot_videos)} videos to {len(phone_ids)} phones")
            
            # Post this slot's videos to phones
            post_resp = requests.post(
                f"{internal_base}/api/videos/post/batch",
                json={
                    "videos": slot_videos,
                    "phone_ids": phone_ids,
                    "caption": "",
                    "hashtags": "#teamwork #teamworktrend #teamworkchallenge #teamworkmakesthedream #letsgo",
                    "auto_start": True,
                    "auto_stop": True,
                    "auto_delete": config["auto_delete"],
                    "distribute_mode": "round_robin"
                },
                timeout=30
            )
            
            duration = time.time() - start_time
            
            if post_resp.status_code == 200:
                result = post_resp.json()
                job_id = result.get("job_id", "unknown")
                self._log_pipeline(db, "posting", "completed",
                                   details={
                                       "job_id": job_id,
                                       "videos_posted": len(slot_videos),
                                       "total_available": len(all_video_filenames),
                                       "slot": slot_index + 1,
                                       "phone_count": len(phone_ids),
                                   },
                                   duration=duration)
                logger.info(f"Posting job started: {job_id} (slot {slot_index + 1}/{num_slots}, {len(slot_videos)} videos)")
            else:
                raise Exception(f"Posting failed: {post_resp.status_code} - {post_resp.text}")
            
        except Exception as e:
            logger.error(f"Posting phase crashed: {e}")
            self._log_pipeline(db, "posting", "failed", error=str(e))
        finally:
            db.close()
    
    # =====================================================================
    # Monitoring Jobs
    # =====================================================================
    
    def check_pending_tasks(self):
        """Check status of pending GeeLark tasks."""
        db = self._get_db()
        try:
            from app.models.account import ActivityLog
            pending = db.query(ActivityLog).filter(
                ActivityLog.success == None,
                ActivityLog.geelark_task_id != None
            ).all()
            
            if not pending:
                return
            
            task_ids = [p.geelark_task_id for p in pending]
            logger.debug(f"Checking {len(task_ids)} pending tasks")
            
            response = self.geelark.query_tasks(task_ids)
            if response.success and response.data:
                for task_data in response.data:
                    task_id = task_data.get("taskId")
                    status = task_data.get("status")
                    
                    log = next((p for p in pending if p.geelark_task_id == task_id), None)
                    if log and status is not None:
                        if status == 2:  # Success
                            log.success = True
                        elif status in (3, 4):  # Failed/Cancelled
                            log.success = False
                            log.error_message = task_data.get("failReason", "Unknown")
                
                db.commit()
                
        except Exception as e:
            logger.error(f"Task check failed: {e}")
        finally:
            db.close()
    
    # =====================================================================
    # Scheduler Control
    # =====================================================================
    
    def start(self):
        """Start the scheduler with configured jobs."""
        if self._running:
            logger.warning("Scheduler already running")
            return
        
        config = self._get_config()
        
        # Phase 1: Warmup
        warmup_utc = est_to_utc(config["warmup_hour_est"])
        self.scheduler.add_job(
            self.run_daily_warmup,
            CronTrigger(hour=warmup_utc, minute=0),
            id="daily_warmup",
            replace_existing=True,
            max_instances=1
        )
        
        # Phase 2: Video Generation
        vidgen_utc = est_to_utc(config["video_gen_hour_est"])
        self.scheduler.add_job(
            self.run_daily_video_generation,
            CronTrigger(hour=vidgen_utc, minute=0),
            id="daily_video_generation",
            replace_existing=True,
            max_instances=1
        )
        
        # Phase 3: Posting (multiple times per day)
        posting_hours = config["posting_hours_est"]
        posting_utc = ",".join(str(est_to_utc(int(h.strip()))) for h in posting_hours.split(","))
        self.scheduler.add_job(
            self.run_auto_posting,
            CronTrigger(hour=posting_utc),
            id="auto_posting",
            replace_existing=True,
            max_instances=1
        )
        
        # Monitoring: check pending tasks every 5 min
        self.scheduler.add_job(
            self.check_pending_tasks,
            IntervalTrigger(minutes=5),
            id="task_monitor",
            replace_existing=True,
            max_instances=1
        )
        
        self.scheduler.start()
        self._running = True
        
        logger.info(f"Scheduler started — Pipeline times (EST):")
        logger.info(f"  Warmup:     {config['warmup_hour_est']}:00 AM EST")
        logger.info(f"  Video Gen:  {config['video_gen_hour_est']}:00 AM EST")
        logger.info(f"  Posting:    {posting_hours} EST")
    
    def stop(self):
        """Stop the scheduler."""
        if self._running:
            self.scheduler.shutdown(wait=False)
            self._running = False
            logger.info("Scheduler stopped")
    
    def get_jobs(self) -> List[dict]:
        """Get list of scheduled jobs with next run times."""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name or job.id,
                "next_run": str(job.next_run_time) if job.next_run_time else None,
                "pending": job.pending,
            })
        return jobs
    
    def run_job_now(self, job_id: str):
        """Manually trigger a job to run immediately."""
        job = self.scheduler.get_job(job_id)
        if job:
            job.modify(next_run_time=datetime.now())
            logger.info(f"Triggered job: {job_id}")
            return True
        return False


# Singleton
_scheduler_instance: Optional[AutomationScheduler] = None


def get_scheduler(geelark_client: GeeLarkClient = None) -> AutomationScheduler:
    """Get or create scheduler singleton."""
    global _scheduler_instance
    if _scheduler_instance is None and geelark_client:
        _scheduler_instance = AutomationScheduler(geelark_client)
    return _scheduler_instance
