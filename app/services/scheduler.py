"""
JesusAI Scheduler — TAP Method
==============================
Lifecycle-aware daily pipeline implementing the TAP growing-accounts method.

Per-account day tracking:
  Day 1-2  -> Light warmup only (10min, scroll-heavy, 1-3 actions max). NO posting.
  Day 3-6  -> Moderate warmup (15min, light engagement). NO posting yet.
              User manually does profile setup (PFP, bio, username, display name)
              spread across these days — dashboard surfaces a checklist.
  Day 7    -> First post day. Continue moderate warmup.
  Day 7+   -> Posts per day scales: every 3 days +1, capped at 4.
              Day 7-9: 1/day, Day 10-12: 2/day, Day 13-15: 3/day, Day 16+: 4/day.

Pipeline (all times EST, configurable):
  1. Warmup        — 8:00 AM
  2. Video Gen     — 9:00 AM
  3. Posting       — 10 AM, 1 PM, 5 PM (3 slots)
  4. Snapshot      — 11 PM

Master switch: ScheduleConfig.enabled.
Per-account switches: Account.schedule_enabled / schedule_warmup / schedule_posting.
"""

import os
import time
from datetime import date, datetime, timedelta, timezone
from typing import List, Optional

from apscheduler.executors.pool import ThreadPoolExecutor as APSThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.account import Account, AccountStatus, PipelineLog, ScheduleConfig
from app.services.phone_provider import get_phone_client

EST_OFFSET = 5  # UTC-5 (no DST)


def est_to_utc(est_hour: int) -> int:
    return (est_hour + EST_OFFSET) % 24


# =============================================================================
# TAP method helpers
# =============================================================================

def posts_per_day_for_day(day: int) -> int:
    """
    TAP scaling: 1 post on Day 7, +1 every 3 days, cap 4.
    Day 1-6: 0 (no posting yet)
    Day 7-9: 1
    Day 10-12: 2
    Day 13-15: 3
    Day 16+: 4
    """
    if day < 7:
        return 0
    return min(4, 1 + (day - 7) // 3)


def warmup_intensity_for_day(day: int) -> dict:
    """
    Returns warmup task settings strictly per TAP method PDF.

    PDF rules:
      Day 1-2: 10+ min FYP scroll. Mostly scrolling. ONLY 1-3 actions max
               (like / save / follow). NO comments. No spam.
      Day 3-6: Continue light warmup daily (10+ min scroll, 1-3 actions).
               Profile setup (PFP/bio/username/display name) is done MANUALLY
               by the user across these days, in separate sessions.
      Day 7+:  First post day. After posting starts, warmup becomes a BRIEF
               engagement session — NOT a heavy session. The account doesn't
               need much warmup once posting begins; it just needs a quick
               daily presence to stay active.

    Returns dict with:
      duration_min, like_chance, comment_chance, enable_likes, enable_comments,
      enable_follow_back, action
    """
    if day <= 2:
        # Day 1-2: scroll-only, NO comments, 1-3 actions max for the whole 10min
        return {
            "duration_min": 10,
            "action": "browse video",
            "like_chance": 6,            # ~1-3 likes per 10min session
            "comment_chance": 0,
            "enable_likes": True,
            "enable_comments": False,
            "enable_follow_back": False,
        }
    if day <= 6:
        # Day 3-6: still light — same caution as Day 1-2.
        # Profile setup (PFP/bio/username/display name) is done manually by the user
        # in separate sessions during this window.
        return {
            "duration_min": 10,
            "action": "browse video",
            "like_chance": 8,            # still ~1-3 actions per session
            "comment_chance": 0,
            "enable_likes": True,
            "enable_comments": False,
            "enable_follow_back": False,
        }
    # Day 7+: brief engagement session — posting is the main activity now.
    # Per user direction: "we don't need much warming up after we start posting".
    return {
        "duration_min": 8,
        "action": "browse video",
        "like_chance": 15,
        "comment_chance": 3,
        "enable_likes": True,
        "enable_comments": True,
        "enable_follow_back": True,
    }


def profile_setup_step_for_day(day: int) -> Optional[str]:
    """Return the profile-setup step the user should do MANUALLY on this day, if any."""
    return {
        3: "Add Profile Picture (PFP)",
        4: "Add Bio",
        5: "Set Username",
        6: "Set Display Name",
    }.get(day)


def increment_warmup_day(account: Account) -> int:
    """Increment & persist warmup_day on the account. Returns new day value."""
    today = date.today()
    last = account.last_activity.date() if account.last_activity else None
    if last == today:
        return account.warmup_day or 0
    account.warmup_day = (account.warmup_day or 0) + 1
    account.last_activity = datetime.utcnow()
    if account.warmup_day >= 7 and not account.warmup_complete:
        account.warmup_complete = True
    if account.warmup_day == 1 and not account.warmup_start_date:
        account.warmup_start_date = datetime.utcnow()
    return account.warmup_day


# =============================================================================
# Scheduler
# =============================================================================

class AutomationScheduler:
    """Lifecycle-aware background scheduler for the JesusAI TAP pipeline."""

    def __init__(self, phone_client=None):
        self.settings = get_settings()
        self.phone_client = phone_client or get_phone_client()
        # Default APScheduler pool is 10 threads; bump to 20 since the API
        # service has 2GB RAM and we run multiple concurrent kie.ai polls
        # plus parallel warmup buckets and the auto-stop callback jobs.
        try:
            pool_size = int(os.getenv("APSCHEDULER_THREAD_POOL", "20"))
        except ValueError:
            pool_size = 20
        executors = {"default": APSThreadPoolExecutor(max_workers=pool_size)}
        self.scheduler = BackgroundScheduler(executors=executors)
        self._running = False
        self._active_warmup_phones: List[str] = []
        logger.info(f"AutomationScheduler (TAP method) initialized — pool={pool_size}")

    # ---- DB helpers --------------------------------------------------------

    def _get_db(self) -> Session:
        return SessionLocal()

    def _get_config(self, db: Optional[Session] = None) -> dict:
        close = db is None
        if close:
            db = self._get_db()
        try:
            cfg = db.query(ScheduleConfig).filter(ScheduleConfig.key == "main").first()
            if cfg:
                return {
                    "enabled": cfg.enabled,
                    "posts_per_phone": cfg.posts_per_phone,
                    "enable_warmup": cfg.enable_warmup,
                    "auto_delete": cfg.auto_delete,
                    "warmup_hour_est": cfg.warmup_hour_est or 8,
                    "video_gen_hour_est": cfg.video_gen_hour_est or 9,
                    "posting_hours_est": cfg.posting_hours_est or "10,13,17",
                    "phone_ids": cfg.phone_ids or [],
                }
            return {
                "enabled": False,
                "posts_per_phone": 1,
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
        q = db.query(Account).filter(Account.schedule_enabled.is_(True))
        if phase == "warmup":
            q = q.filter(Account.schedule_warmup.is_(True))
        elif phase == "posting":
            q = q.filter(Account.schedule_posting.is_(True))
        return q.all()

    def _log_pipeline(
        self,
        db: Session,
        phase: str,
        status: str,
        phone_id: Optional[str] = None,
        account_name: Optional[str] = None,
        details: Optional[dict] = None,
        error: Optional[str] = None,
        duration: Optional[float] = None,
    ) -> PipelineLog:
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
    # Phase 1: Daily Warmup (TAP-aware)
    # =====================================================================

    def run_daily_warmup(self):
        logger.info("=" * 50)
        logger.info("PIPELINE PHASE 1: TAP Warmup")
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
                self._log_pipeline(db, "warmup", "skipped", details={"reason": "no_accounts"})
                return

            # Bucket accounts by intensity (Day 1-2, 3-6, 7+) so we can dispatch
            # one batch per intensity. Each batch shares duration & like-chance.
            buckets: dict = {}
            profile_steps: List[dict] = []
            for account in accounts:
                if not account.geelark_profile_id:
                    logger.warning(f"Account {account.id} has no GeeLark profile — skipping")
                    continue
                day = increment_warmup_day(account)
                intensity = warmup_intensity_for_day(day)
                key = (
                    intensity["duration_min"],
                    intensity["action"],
                    intensity["like_chance"],
                    intensity["comment_chance"],
                    intensity["enable_likes"],
                    intensity["enable_comments"],
                    intensity["enable_follow_back"],
                )
                buckets.setdefault(key, []).append(account)

                step = profile_setup_step_for_day(day)
                if step:
                    profile_steps.append({
                        "account_id": account.id,
                        "username": account.tiktok_username or account.geelark_profile_name,
                        "day": day,
                        "step": step,
                    })

            db.commit()

            if not buckets:
                logger.warning("No valid phones for warmup")
                self._log_pipeline(db, "warmup", "skipped", details={"reason": "no_phones"})
                return

            # Surface profile-setup TODOs to the pipeline log so the dashboard can show them
            if profile_steps:
                self._log_pipeline(
                    db, "profile_setup", "todo",
                    details={"steps": profile_steps},
                )

            self._log_pipeline(
                db, "warmup", "started",
                details={
                    "buckets": [
                        {"intensity": list(k), "count": len(v)}
                        for k, v in buckets.items()
                    ],
                    "total_accounts": sum(len(v) for v in buckets.values()),
                },
            )

            start_time = time.time()
            all_phone_ids: List[str] = []
            max_duration = 0

            for key, group in buckets.items():
                duration_min, action, like_chance, comment_chance, en_likes, en_comments, en_follow = key
                phone_ids = [a.geelark_profile_id for a in group]
                all_phone_ids.extend(phone_ids)
                max_duration = max(max_duration, duration_min)

                logger.info(
                    f"Bucket: {len(phone_ids)} phones | {duration_min}min | "
                    f"like_chance={like_chance} comment_chance={comment_chance}"
                )

                # Boot the phones in this bucket
                try:
                    start_resp = self.phone_client.start_phones(phone_ids)
                    if not start_resp.success:
                        raise Exception(f"start_phones: {start_resp.message}")
                except Exception as e:
                    logger.error(f"Phone start failed for bucket: {e}")
                    self._log_pipeline(db, "warmup", "failed", error=str(e))
                    continue

                # Submit the warmup task chain
                try:
                    self.phone_client.run_enhanced_warmup(
                        phone_ids=phone_ids,
                        duration_minutes=duration_min,
                        keywords=None,  # uses JesusAI defaults inside the client
                        enable_comments=en_comments,
                        enable_likes=en_likes,
                        enable_follow_back=en_follow,
                        like_probability=like_chance,
                        comment_chance=comment_chance,  # TAP-scaled, was hardcoded 15
                    )
                except Exception as e:
                    logger.error(f"Warmup task chain submit failed: {e}")
                    try:
                        self.phone_client.stop_phones(phone_ids)
                    except Exception:
                        pass
                    continue

            self._active_warmup_phones = all_phone_ids[:]

            # Schedule auto-stop for max bucket duration + 5min buffer
            stop_delay_seconds = (max_duration + 5) * 60
            try:
                stop_time = datetime.now() + timedelta(seconds=stop_delay_seconds)
                self.scheduler.add_job(
                    self._stop_warmup_phones,
                    trigger="date",
                    run_date=stop_time,
                    args=[all_phone_ids],
                    id=f"warmup_stop_{int(time.time())}",
                    replace_existing=False,
                    max_instances=1,
                )
                logger.info(f"Auto-stop scheduled in {max_duration + 5}min")
            except Exception as e:
                logger.warning(f"Could not schedule auto-stop: {e}")

            duration = time.time() - start_time
            self._log_pipeline(
                db, "warmup", "completed",
                details={
                    "phone_count": len(all_phone_ids),
                    "max_duration_min": max_duration,
                    "auto_stop_in_min": max_duration + 5,
                    "profile_setup_steps": len(profile_steps),
                },
                duration=duration,
            )
            logger.info(f"Warmup phase complete: {len(all_phone_ids)} phones running")

        except Exception as e:
            logger.error(f"Warmup phase crashed: {e}")
            self._log_pipeline(db, "warmup", "failed", error=str(e))
        finally:
            db.close()

    def _stop_warmup_phones(self, phone_ids: list):
        logger.info(f"Auto-stopping {len(phone_ids)} phones after warmup...")
        try:
            resp = self.phone_client.stop_phones(phone_ids)
            if resp.success:
                logger.info(f"  ✓ Stopped {len(phone_ids)} phones")
            else:
                logger.warning(f"  ⚠ Stop response: {resp.message}")
        except Exception as e:
            logger.error(f"Stop failed: {e}")
        finally:
            self._active_warmup_phones = []

    def stop_warmup_now(self):
        phone_ids = list(self._active_warmup_phones)
        if not phone_ids:
            return {"stopped": 0, "message": "No active warmup phones"}

        # Cancel pending auto-stop jobs
        try:
            for job in self.scheduler.get_jobs():
                if job.id.startswith("warmup_stop_"):
                    job.remove()
        except Exception as e:
            logger.warning(f"Couldn't cancel pending jobs: {e}")

        try:
            resp = self.phone_client.stop_phones(phone_ids)
            self._active_warmup_phones = []
            if resp.success:
                return {"stopped": len(phone_ids), "message": f"Stopped {len(phone_ids)} phones"}
            return {"stopped": 0, "message": f"Stop failed: {resp.message}"}
        except Exception as e:
            return {"stopped": 0, "message": f"Error: {e}"}

    # =====================================================================
    # Phase 2: Video Generation (lifecycle-aware demand)
    # =====================================================================

    def run_daily_video_generation(self):
        logger.info("=" * 50)
        logger.info("PIPELINE PHASE 2: JesusAI Video Generation")
        logger.info("=" * 50)

        config = self._get_config()
        if not config["enabled"]:
            logger.info("Pipeline DISABLED — skipping video gen")
            return

        db = self._get_db()
        try:
            accounts = self._get_scheduled_accounts(db, "posting")
            if not accounts:
                self._log_pipeline(db, "video_gen", "skipped", details={"reason": "no_accounts"})
                return

            # Compute demand: sum posts/day across accounts past Day 7
            demand = 0
            ready_accounts = 0
            for a in accounts:
                day = a.warmup_day or 0
                ppd = posts_per_day_for_day(day)
                if ppd > 0:
                    demand += ppd
                    ready_accounts += 1

            if demand == 0:
                logger.info("No accounts past Day 7 yet — skipping video gen")
                self._log_pipeline(db, "video_gen", "skipped",
                                   details={"reason": "no_accounts_ready_to_post"})
                return

            from app.services.video_generator import get_video_generator
            generator = get_video_generator()

            # Cap library at 100 videos to avoid runaway costs
            VIDEO_LIBRARY_CAP = 100
            existing = list(generator.output_dir.glob("jesusai_*.mp4")) + \
                       list(generator.output_dir.glob("teamwork_*.mp4"))
            room = max(0, VIDEO_LIBRARY_CAP - len(existing))

            target = min(demand, room)
            if target == 0:
                logger.info(f"Library full ({len(existing)}/{VIDEO_LIBRARY_CAP}) — skipping")
                self._log_pipeline(db, "video_gen", "skipped",
                                   details={"reason": "library_full", "existing": len(existing)})
                return

            logger.info(f"Generating {target} videos (demand={demand}, room={room}, ready={ready_accounts})")
            self._log_pipeline(db, "video_gen", "started",
                               details={"target": target, "demand": demand, "ready_accounts": ready_accounts})

            start_time = time.time()
            results = generator.generate_batch(count=target, mode="realistic")
            successful = sum(1 for r in results if r.success)
            failed = len(results) - successful
            total_cost = sum(r.cost_usd for r in results)
            duration = time.time() - start_time

            self._log_pipeline(
                db, "video_gen", "completed",
                details={
                    "videos_generated": successful,
                    "videos_failed": failed,
                    "cost_usd": round(total_cost, 2),
                    "model": "nano-banana-pro-2K + " + generator.DEFAULT_VIDEO_MODEL,
                },
                duration=duration,
            )
            logger.info(
                f"Video gen complete: {successful} ok / {failed} failed / "
                f"${total_cost:.2f} / {duration:.0f}s"
            )

        except Exception as e:
            logger.error(f"Video gen crashed: {e}")
            self._log_pipeline(db, "video_gen", "failed", error=str(e))
        finally:
            db.close()

    # =====================================================================
    # Phase 3: Posting (TAP-scaled per account)
    # =====================================================================

    def run_auto_posting(self):
        logger.info("=" * 50)
        logger.info("PIPELINE PHASE 3: TAP Posting")
        logger.info("=" * 50)

        config = self._get_config()
        if not config["enabled"]:
            logger.info("Pipeline DISABLED — skipping posting")
            return

        db = self._get_db()
        try:
            accounts = self._get_scheduled_accounts(db, "posting")
            if not accounts:
                self._log_pipeline(db, "posting", "skipped", details={"reason": "no_accounts"})
                return

            # Determine current slot index based on EST hour
            posting_hours = [int(h.strip()) for h in config["posting_hours_est"].split(",")]
            num_slots = max(1, len(posting_hours))
            est = timezone(timedelta(hours=-EST_OFFSET))
            cur_hour = datetime.now(est).hour

            slot_index = 0
            for i, h in enumerate(posting_hours):
                if abs(cur_hour - h) <= 1:
                    slot_index = i
                    break

            logger.info(f"Slot {slot_index + 1}/{num_slots} (EST hour: {cur_hour})")

            # Compute per-account posts for THIS slot
            schedule_assignments = []  # list of (phone_id, posts_this_slot)
            for a in accounts:
                if not a.geelark_profile_id:
                    continue
                day = a.warmup_day or 0
                ppd = posts_per_day_for_day(day)
                if ppd == 0:
                    continue
                # Spread ppd evenly across slots
                base = ppd // num_slots
                # Distribute remainder to earliest slots
                extra = 1 if slot_index < (ppd - base * num_slots) else 0
                this_slot = base + extra
                if this_slot > 0:
                    schedule_assignments.append((a.geelark_profile_id, this_slot, a.tiktok_username or a.geelark_profile_name))

            if not schedule_assignments:
                logger.info(f"Slot {slot_index + 1}: no accounts due to post")
                self._log_pipeline(db, "posting", "skipped",
                                   details={"reason": "no_accounts_for_slot", "slot": slot_index + 1})
                return

            total_videos_needed = sum(n for _, n, _ in schedule_assignments)

            self._log_pipeline(db, "posting", "started",
                               details={"slot": slot_index + 1, "total_slots": num_slots,
                                        "videos_needed": total_videos_needed,
                                        "accounts": len(schedule_assignments)})

            import requests
            internal_base = os.getenv("RENDER_EXTERNAL_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")

            # Fetch available videos
            videos_resp = requests.get(f"{internal_base}/api/videos/list", timeout=10)
            if videos_resp.status_code != 200:
                raise Exception(f"video list fetch failed: {videos_resp.status_code}")
            all_videos = [v["filename"] for v in videos_resp.json().get("videos", [])]
            if not all_videos:
                logger.warning("No videos available")
                self._log_pipeline(db, "posting", "skipped", details={"reason": "no_videos"})
                return

            videos_to_use = all_videos[:total_videos_needed]
            if len(videos_to_use) < total_videos_needed:
                logger.warning(
                    f"Only {len(videos_to_use)}/{total_videos_needed} videos available — partial post"
                )

            # Build flat assignment: position i in assignment_phones receives videos_to_use[i].
            # Phone with N posts in this slot appears N times — paired 1-to-1 with videos.
            assignment_phones: List[str] = []
            for phone_id, n, _name in schedule_assignments:
                assignment_phones.extend([phone_id] * n)
            # Truncate to actual video count if we're short
            assignment_phones = assignment_phones[:len(videos_to_use)]

            start_time = time.time()
            post_resp = requests.post(
                f"{internal_base}/api/videos/post/batch",
                json={
                    "videos": videos_to_use,
                    "phone_ids": assignment_phones,  # multiset — same length as videos
                    "caption": "",
                    "hashtags": "#jesus #jesussaves #jesuslovesyou #fyp #foryou #christian",
                    "auto_start": True,
                    "auto_stop": True,
                    "auto_delete": config["auto_delete"],
                    "distribute_mode": "one_to_one",  # respects per-phone count
                },
                timeout=30,
            )

            duration = time.time() - start_time
            if post_resp.status_code == 200:
                result = post_resp.json()
                self._log_pipeline(db, "posting", "completed",
                                   details={
                                       "job_id": result.get("job_id"),
                                       "videos_posted": len(videos_to_use),
                                       "slot": slot_index + 1,
                                   },
                                   duration=duration)
                logger.info(f"Posting job started: {result.get('job_id')} — {len(videos_to_use)} videos")
            else:
                raise Exception(f"posting failed: {post_resp.status_code} {post_resp.text}")

        except Exception as e:
            logger.error(f"Posting phase crashed: {e}")
            self._log_pipeline(db, "posting", "failed", error=str(e))
        finally:
            db.close()

    # =====================================================================
    # Monitoring
    # =====================================================================

    def check_pending_tasks(self):
        db = self._get_db()
        try:
            from app.models.account import ActivityLog
            pending = db.query(ActivityLog).filter(
                ActivityLog.success.is_(None),
                ActivityLog.geelark_task_id.isnot(None),
            ).all()
            if not pending:
                return

            task_ids = [p.geelark_task_id for p in pending]
            response = self.phone_client.query_tasks(task_ids)
            if response.success and response.data:
                for task_data in response.data:
                    tid = task_data.get("taskId")
                    status = task_data.get("status")
                    log = next((p for p in pending if p.geelark_task_id == tid), None)
                    if log and status is not None:
                        if status == 2:
                            log.success = True
                        elif status in (3, 4):
                            log.success = False
                            log.error_message = task_data.get("failReason", "Unknown")
                db.commit()
        except Exception as e:
            logger.error(f"Task monitor failed: {e}")
        finally:
            db.close()

    def take_follower_snapshot(self):
        try:
            import requests as req
            internal_base = os.getenv("RENDER_EXTERNAL_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")
            resp = req.post(f"{internal_base}/api/followers/snapshot", timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                logger.info(f"Snapshot: {data.get('accounts_tracked', 0)} accounts tracked")
            else:
                logger.error(f"Snapshot failed: {resp.status_code}")
        except Exception as e:
            logger.error(f"Snapshot error: {e}")

    # =====================================================================
    # Scheduler control
    # =====================================================================

    def start(self):
        if self._running:
            logger.warning("Scheduler already running")
            return

        config = self._get_config()
        warmup_utc = est_to_utc(config["warmup_hour_est"])
        vidgen_utc = est_to_utc(config["video_gen_hour_est"])
        posting_hours = config["posting_hours_est"]
        posting_utc = ",".join(str(est_to_utc(int(h.strip()))) for h in posting_hours.split(","))

        self.scheduler.add_job(self.run_daily_warmup, CronTrigger(hour=warmup_utc, minute=0),
                               id="daily_warmup", replace_existing=True, max_instances=1)
        self.scheduler.add_job(self.run_daily_video_generation, CronTrigger(hour=vidgen_utc, minute=0),
                               id="daily_video_generation", replace_existing=True, max_instances=1)
        self.scheduler.add_job(self.run_auto_posting, CronTrigger(hour=posting_utc),
                               id="auto_posting", replace_existing=True, max_instances=1)
        self.scheduler.add_job(self.check_pending_tasks, IntervalTrigger(minutes=5),
                               id="task_monitor", replace_existing=True, max_instances=1)
        self.scheduler.add_job(self.take_follower_snapshot, CronTrigger(hour=est_to_utc(23), minute=0),
                               id="follower_snapshot", replace_existing=True, max_instances=1)

        self.scheduler.start()
        self._running = True

        logger.info("Scheduler started — pipeline (EST):")
        logger.info(f"  Warmup:    {config['warmup_hour_est']}:00 (TAP-aware)")
        logger.info(f"  Video Gen: {config['video_gen_hour_est']}:00")
        logger.info(f"  Posting:   {posting_hours}")

    def stop(self):
        if self._running:
            self.scheduler.shutdown(wait=False)
            self._running = False
            logger.info("Scheduler stopped")

    def get_jobs(self) -> List[dict]:
        return [
            {
                "id": j.id,
                "name": j.name or j.id,
                "next_run": str(j.next_run_time) if j.next_run_time else None,
                "pending": j.pending,
            }
            for j in self.scheduler.get_jobs()
        ]

    def run_job_now(self, job_id: str) -> bool:
        job = self.scheduler.get_job(job_id)
        if job:
            job.modify(next_run_time=datetime.now())
            return True
        return False


# =============================================================================
# Singleton
# =============================================================================

_scheduler_instance: Optional[AutomationScheduler] = None


def get_scheduler(phone_client=None) -> AutomationScheduler:
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = AutomationScheduler(phone_client)
    return _scheduler_instance
