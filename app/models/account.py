"""
Account and Related Models
==========================
Database models for accounts, proxies, videos, and activity tracking.
"""

import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date,
    ForeignKey, Text, Enum, JSON, Float
)
from sqlalchemy.orm import relationship
from app.database import Base


class AccountStatus(enum.Enum):
    """Account lifecycle status."""
    CREATED = "created"
    WARMING_UP = "warming_up"
    ACTIVE = "active"
    POSTING = "posting"
    PAUSED = "paused"
    BANNED = "banned"
    ERROR = "error"


class ScheduleType(enum.Enum):
    """Types of scheduled tasks."""
    WARMUP = "warmup"
    POST_VIDEO = "post_video"
    ENGAGEMENT = "engagement"


class Proxy(Base):
    """Proxiware proxy configuration."""
    __tablename__ = "proxies"
    
    id = Column(Integer, primary_key=True, index=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    protocol = Column(String(10), default="HTTP")  # HTTP, SOCKS5
    location = Column(String(100), nullable=True)  # e.g., "US", "UK"
    is_assigned = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_tested = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    accounts = relationship("Account", back_populates="proxy")
    
    def to_geelark_format(self) -> dict:
        """Convert to GeeLark proxy config format."""
        return {
            "proxyType": self.protocol.lower(),
            "proxyHost": self.host,
            "proxyPort": self.port,
            "proxyUser": self.username or "",
            "proxyPassword": self.password or ""
        }


class Account(Base):
    """TikTok account linked to GeeLark cloud phone."""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # GeeLark Profile Info
    geelark_profile_id = Column(String(100), unique=True, nullable=True)
    geelark_profile_name = Column(String(255), nullable=True)
    
    # TikTok Account Info
    tiktok_username = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    password = Column(String(255), nullable=True)  # Consider encryption in prod
    
    # Status & Metrics
    status = Column(Enum(AccountStatus), default=AccountStatus.CREATED)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    likes_given = Column(Integer, default=0)
    
    # Warmup Tracking
    warmup_start_date = Column(DateTime, nullable=True)
    warmup_day = Column(Integer, default=0)
    warmup_complete = Column(Boolean, default=False)
    
    # Timestamps
    last_activity = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    proxy_id = Column(Integer, ForeignKey("proxies.id"), nullable=True)
    
    # Relationships
    proxy = relationship("Proxy", back_populates="accounts")
    videos = relationship("Video", back_populates="account")
    activity_logs = relationship("ActivityLog", back_populates="account")
    schedules = relationship("Schedule", back_populates="account")
    
    # Additional config stored as JSON
    device_config = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Per-account scheduling (v2.0)
    schedule_enabled = Column(Boolean, default=False)   # Master toggle for daily pipeline
    schedule_warmup = Column(Boolean, default=True)     # Include in warmup phase
    schedule_posting = Column(Boolean, default=True)    # Include in posting phase


class Video(Base):
    """Videos for auto-posting."""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # File Info
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Posting Info
    caption = Column(Text, nullable=True)
    hashtags = Column(Text, nullable=True)  # Comma-separated
    sound_id = Column(String(100), nullable=True)
    
    # Status
    is_uploaded_to_phone = Column(Boolean, default=False)
    geelark_resource_url = Column(String(500), nullable=True)
    is_posted = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    tiktok_video_id = Column(String(100), nullable=True)
    
    # Metrics (if we can track)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    
    # Foreign Key
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    
    # Relationships
    account = relationship("Account", back_populates="videos")
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ActivityLog(Base):
    """Log all automation activities for monitoring."""
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Activity Info
    action_type = Column(String(50), nullable=False)  # warmup, post, like, follow, etc.
    action_details = Column(JSON, nullable=True)
    
    # GeeLark Task Info
    geelark_task_id = Column(String(100), nullable=True)
    flow_name = Column(String(100), nullable=True)
    
    # Result
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Foreign Key
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="activity_logs")
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Schedule(Base):
    """Scheduled automation tasks."""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    
    # Scheduling Info
    cron_expression = Column(String(100), nullable=True)  # For complex schedules
    run_at = Column(DateTime, nullable=True)  # For one-time runs
    repeat_daily = Column(Boolean, default=True)
    
    # Config
    config = Column(JSON, nullable=True)  # Action limits, delays, etc.
    
    # Status
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    run_count = Column(Integer, default=0)
    
    # Foreign Key
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="schedules")
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ScheduleConfig(Base):
    """
    Global scheduling configuration - stored in DB for persistence.
    This survives page refreshes and is readable by the backend scheduler.
    """
    __tablename__ = "schedule_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, nullable=False, default="main")
    
    # Scheduling State
    enabled = Column(Boolean, default=False)
    phone_ids = Column(JSON, default=[])  # Legacy — v2.0 uses per-account scheduling
    
    # Configuration
    posts_per_phone = Column(Integer, default=3)
    enable_warmup = Column(Boolean, default=True)
    auto_delete = Column(Boolean, default=True)
    
    # Pipeline timing (EST hours, stored as integers)
    warmup_hour_est = Column(Integer, default=8)       # 8 AM EST
    video_gen_hour_est = Column(Integer, default=9)    # 9 AM EST
    posting_hours_est = Column(String(50), default="10,13,17")  # 10 AM, 1 PM, 5 PM EST
    
    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class PipelineLog(Base):
    """
    Log every automated pipeline action for monitoring.
    Tracks warmup, video generation, and posting phases.
    """
    __tablename__ = "pipeline_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Pipeline info
    pipeline_date = Column(Date, nullable=False)   # The date this pipeline ran
    phase = Column(String(30), nullable=False)      # warmup, video_gen, posting
    
    # Target
    phone_id = Column(String(100), nullable=True)   # GeeLark phone ID
    account_name = Column(String(255), nullable=True)  # Human-readable name
    
    # Status
    status = Column(String(20), nullable=False, default="started")  # started, completed, failed, skipped
    
    # Details
    details = Column(JSON, nullable=True)           # Phase-specific data
    error_message = Column(Text, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class FollowerSnapshot(Base):
    """
    Daily follower count snapshot per account.
    Used to track growth over time and display charts on the dashboard.
    """
    __tablename__ = "follower_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    snapshot_date = Column(Date, nullable=False)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    account = relationship("Account")
