"""
Warmup Service
==============
Handles TikTok account warmup automation with progressive engagement.
"""

import random
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from loguru import logger

from app.models.account import Account, AccountStatus, ActivityLog, Schedule, ScheduleType
from app.services.geelark_client import GeeLarkClient
from app.config import get_settings

settings = get_settings()


class WarmupService:
    """
    Manages TikTok account warmup through progressive engagement.
    
    Warmup Strategy (default 5 days):
    - Day 1-2: Scroll feed, watch videos (passive)
    - Day 3-4: Add likes (10-30), light follows (5-10)
    - Day 5+: Full engagement (follows, likes, comments)
    """
    
    # Warmup configuration per day
    WARMUP_CONFIG = {
        1: {"duration_min": 30, "max_likes": 5, "max_follows": 0, "max_comments": 0},
        2: {"duration_min": 40, "max_likes": 10, "max_follows": 2, "max_comments": 0},
        3: {"duration_min": 45, "max_likes": 20, "max_follows": 5, "max_comments": 2},
        4: {"duration_min": 50, "max_likes": 30, "max_follows": 10, "max_comments": 3},
        5: {"duration_min": 60, "max_likes": 40, "max_follows": 15, "max_comments": 5},
    }
    
    def __init__(self, db: Session, geelark_client: GeeLarkClient):
        self.db = db
        self.geelark = geelark_client
        self.warmup_days = settings.warmup_days
    
    def start_warmup(self, account_id: int) -> bool:
        """
        Initialize warmup for an account.
        
        Sets status to WARMING_UP and records start date.
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False
        
        account.status = AccountStatus.WARMING_UP
        account.warmup_start_date = datetime.utcnow()
        account.warmup_day = 1
        account.warmup_complete = False
        self.db.commit()
        
        self._log_activity(account_id, "warmup_started", {
            "start_date": account.warmup_start_date.isoformat()
        })
        
        logger.info(f"Started warmup for account {account_id}")
        return True
    
    def get_warmup_config(self, day: int) -> Dict:
        """Get warmup configuration for a specific day."""
        # Use max day config for days beyond defined
        if day > max(self.WARMUP_CONFIG.keys()):
            day = max(self.WARMUP_CONFIG.keys())
        return self.WARMUP_CONFIG.get(day, self.WARMUP_CONFIG[1])
    
    def run_warmup_session(self, account_id: int) -> bool:
        """
        Execute a warmup session for an account.
        
        Uses GeeLark's TikTok AI warmup flow with day-appropriate limits.
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or account.status != AccountStatus.WARMING_UP:
            logger.warning(f"Account {account_id} not ready for warmup")
            return False
        
        if not account.geelark_profile_id:
            logger.error(f"Account {account_id} has no GeeLark profile")
            return False
        
        # Calculate current warmup day
        if account.warmup_start_date:
            days_since_start = (datetime.utcnow() - account.warmup_start_date).days + 1
            account.warmup_day = days_since_start
        else:
            account.warmup_day = 1
        
        # Get config for current day
        config = self.get_warmup_config(account.warmup_day)
        
        # Add randomization to avoid patterns
        config = self._randomize_config(config)
        
        logger.info(
            f"Running warmup day {account.warmup_day} for account {account_id}: "
            f"{config['duration_min']}min browse video"
        )
        
        # Execute warmup flow via GeeLark (browse video action)
        response = self.geelark.run_tiktok_warmup(
            phone_ids=[account.geelark_profile_id],
            duration_minutes=config["duration_min"],
            action="browse video"
        )
        
        if response.success:
            # Update account stats
            account.likes_given += config["max_likes"]
            account.following_count += config["max_follows"]
            account.last_activity = datetime.utcnow()
            
            # Check if warmup complete
            if account.warmup_day >= self.warmup_days:
                self.complete_warmup(account_id)
            
            self.db.commit()
            
            self._log_activity(account_id, "warmup_session", {
                "day": account.warmup_day,
                "task_id": response.data.get("taskId") if response.data else None,
                **config
            })
            
            # ===== AUTO-SHUTDOWN TO SAVE MINUTES =====
            # Stop the phone after warmup to avoid burning subscription time
            logger.info(f"Stopping phone {account.geelark_profile_id} after warmup to save minutes")
            self.geelark.stop_phones([account.geelark_profile_id])
            
            self._log_activity(account_id, "phone_stopped_after_warmup", {
                "day": account.warmup_day,
                "reason": "save_subscription_minutes"
            })
            # ==========================================
            
            return True
        else:
            self._log_activity(
                account_id, "warmup_session",
                {"day": account.warmup_day, "error": response.message},
                success=False,
                error=response.message
            )
            return False
    
    def complete_warmup(self, account_id: int) -> bool:
        """Mark warmup as complete and transition to ACTIVE status."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False
        
        account.warmup_complete = True
        account.status = AccountStatus.ACTIVE
        self.db.commit()
        
        self._log_activity(account_id, "warmup_completed", {
            "total_days": account.warmup_day,
            "total_likes": account.likes_given,
            "total_follows": account.following_count
        })
        
        logger.info(f"Warmup complete for account {account_id}")
        return True
    
    def schedule_warmup(
        self,
        account_id: int,
        run_time: Optional[datetime] = None,
        randomize_time: bool = True
    ) -> Optional[Schedule]:
        """
        Schedule a warmup session.
        
        Args:
            account_id: Account to schedule warmup for
            run_time: Specific time to run (default: now + random offset)
            randomize_time: Add random offset to avoid patterns
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return None
        
        if not run_time:
            run_time = datetime.utcnow()
        
        if randomize_time:
            # Add random offset (0-60 minutes)
            offset_minutes = random.randint(0, 60)
            run_time = run_time + timedelta(minutes=offset_minutes)
        
        schedule = Schedule(
            account_id=account_id,
            schedule_type=ScheduleType.WARMUP,
            run_at=run_time,
            repeat_daily=True,
            is_active=True,
            config={
                "warmup_day": account.warmup_day + 1,
            }
        )
        
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        
        return schedule
    
    def run_batch_warmup(self, account_ids: Optional[List[int]] = None) -> Dict:
        """
        Run warmup for multiple accounts.
        
        Args:
            account_ids: Specific accounts, or None for all warming accounts
        """
        if account_ids:
            accounts = self.db.query(Account).filter(
                Account.id.in_(account_ids),
                Account.status == AccountStatus.WARMING_UP
            ).all()
        else:
            accounts = self.db.query(Account).filter(
                Account.status == AccountStatus.WARMING_UP,
                Account.warmup_complete == False
            ).all()
        
        results = {
            "total": len(accounts),
            "success": 0,
            "failed": 0,
            "completed": 0
        }
        
        for account in accounts:
            success = self.run_warmup_session(account.id)
            if success:
                results["success"] += 1
                if account.warmup_complete:
                    results["completed"] += 1
            else:
                results["failed"] += 1
            
            # Delay between accounts to avoid rate limits
            import time
            delay = random.randint(
                settings.min_delay_seconds,
                settings.max_delay_seconds
            )
            time.sleep(delay)
        
        logger.info(f"Batch warmup complete: {results}")
        return results
    
    def _randomize_config(self, config: Dict) -> Dict:
        """Add randomization to warmup config."""
        return {
            "duration_min": config["duration_min"] + random.randint(-5, 10),
            "max_likes": max(0, config["max_likes"] + random.randint(-3, 3)),
            "max_follows": max(0, config["max_follows"] + random.randint(-2, 2)),
            "max_comments": max(0, config["max_comments"] + random.randint(-1, 1))
        }
    
    def _log_activity(
        self,
        account_id: int,
        action_type: str,
        details: Dict,
        success: bool = True,
        error: Optional[str] = None
    ):
        """Log warmup activity."""
        log = ActivityLog(
            account_id=account_id,
            action_type=action_type,
            action_details=details,
            success=success,
            error_message=error
        )
        self.db.add(log)
        self.db.commit()
