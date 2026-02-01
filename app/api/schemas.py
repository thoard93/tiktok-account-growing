"""
API Schemas
===========
Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# ===========================
# Enums
# ===========================

class AccountStatusEnum(str, Enum):
    CREATED = "created"
    WARMING_UP = "warming_up"
    ACTIVE = "active"
    POSTING = "posting"
    PAUSED = "paused"
    BANNED = "banned"
    ERROR = "error"


class TaskStatusEnum(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ===========================
# Proxy Schemas
# ===========================

class ProxyBase(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "HTTP"
    location: Optional[str] = None


class ProxyCreate(ProxyBase):
    pass


class ProxyBulkCreate(BaseModel):
    """Import proxies from text format: host:port:user:pass per line"""
    proxy_list: str = Field(..., description="Proxies in format host:port:user:pass, one per line")
    protocol: str = "HTTP"


class ProxyResponse(ProxyBase):
    id: int
    is_assigned: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===========================
# Account Schemas
# ===========================

class AccountBase(BaseModel):
    tiktok_username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class AccountCreate(AccountBase):
    name: str = Field(..., description="GeeLark profile name")
    proxy_id: Optional[int] = None


class AccountBatchCreate(BaseModel):
    count: int = Field(..., ge=1, le=100, description="Number of accounts to create")
    name_prefix: str = "TikTok_Account"
    credentials: Optional[List[Dict[str, str]]] = None


class AccountUpdate(BaseModel):
    tiktok_username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class AccountResponse(AccountBase):
    id: int
    geelark_profile_id: Optional[str]
    geelark_profile_name: Optional[str]
    status: AccountStatusEnum
    followers_count: int
    following_count: int
    posts_count: int
    warmup_day: int
    warmup_complete: bool
    last_activity: Optional[datetime]
    created_at: datetime
    proxy: Optional[ProxyResponse] = None
    
    class Config:
        from_attributes = True


class AccountListResponse(BaseModel):
    total: int
    items: List[AccountResponse]


# ===========================
# Video Schemas
# ===========================

class VideoBase(BaseModel):
    caption: Optional[str] = None
    hashtags: Optional[str] = None


class VideoCreate(VideoBase):
    filename: str


class VideoResponse(VideoBase):
    id: int
    filename: str
    filepath: str
    file_size: Optional[int]
    is_uploaded_to_phone: bool
    is_posted: bool
    posted_at: Optional[datetime]
    account_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class VideoListResponse(BaseModel):
    total: int
    items: List[VideoResponse]


# ===========================
# Task/Warmup Schemas
# ===========================

class WarmupStart(BaseModel):
    account_ids: List[int] = Field(..., description="Account IDs to start warmup")


class WarmupSession(BaseModel):
    account_ids: Optional[List[int]] = Field(None, description="Specific accounts or all warming")
    duration_minutes: int = 45
    max_likes: int = 30
    max_follows: int = 10
    max_comments: int = 5


class PostVideoRequest(BaseModel):
    account_id: int
    video_id: int
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    schedule_at: Optional[datetime] = None


class BatchPostRequest(BaseModel):
    account_ids: Optional[List[int]] = None
    videos_per_account: int = 1


# ===========================
# Activity Log Schemas
# ===========================

class ActivityLogResponse(BaseModel):
    id: int
    account_id: int
    action_type: str
    action_details: Optional[Dict[str, Any]]
    success: bool
    error_message: Optional[str]
    geelark_task_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ActivityLogListResponse(BaseModel):
    total: int
    items: List[ActivityLogResponse]


# ===========================
# GeeLark Task Schemas
# ===========================

class GeeLarkTaskResponse(BaseModel):
    id: str
    plan_name: Optional[str] = None
    task_type: int
    task_type_name: str
    serial_name: Optional[str] = None
    env_id: Optional[str] = None
    schedule_at: Optional[int] = None
    status: int
    status_name: str
    fail_code: Optional[int] = None
    fail_desc: Optional[str] = None
    cost: Optional[int] = None
    share_link: Optional[str] = None


class GeeLarkTaskListResponse(BaseModel):
    total: int
    items: List[GeeLarkTaskResponse]


# ===========================
# Schedule Schemas
# ===========================

class ScheduleCreate(BaseModel):
    account_id: int
    schedule_type: str  # warmup, post_video, engagement
    run_at: Optional[datetime] = None
    repeat_daily: bool = True
    config: Optional[Dict[str, Any]] = None


class ScheduleResponse(BaseModel):
    id: int
    account_id: int
    schedule_type: str
    run_at: Optional[datetime]
    repeat_daily: bool
    is_active: bool
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===========================
# Health & Status Schemas
# ===========================

class HealthResponse(BaseModel):
    status: str
    geelark_connected: bool
    database_connected: bool
    accounts_total: int
    accounts_warming: int
    accounts_active: int
    timestamp: datetime


class DashboardStats(BaseModel):
    total_accounts: int
    warming_up: int
    active: int
    posting: int
    paused: int
    banned: int
    total_proxies: int
    available_proxies: int
    total_videos: int
    unposted_videos: int
    recent_posts: int
    tasks_today: int


# ===========================
# GeeLark Direct Schemas
# ===========================

class PhoneCreateRequest(BaseModel):
    name: str
    proxy_string: Optional[str] = None
    mobile_type: str = "Android 12"
    group: Optional[str] = None
    tags: Optional[List[str]] = None
    region: str = "USA-US"
    language: str = "default"


class PhoneStartRequest(BaseModel):
    ids: List[str]
    width: int = 336
    energy_saving_mode: int = 0


class TaskQueryRequest(BaseModel):
    task_ids: List[str] = Field(..., max_length=100)


class TaskCancelRequest(BaseModel):
    task_ids: List[str] = Field(..., max_length=100)


class TaskRetryRequest(BaseModel):
    task_ids: List[str] = Field(..., max_length=100)
