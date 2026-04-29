"""
Application Configuration
=========================
Manages environment variables and application settings.
"""

import os
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Phone Provider: "geelark" or "multilogin"
    phone_provider: str = "geelark"
    
    # GeeLark Auth Method
    geelark_auth_method: Literal["TOKEN", "KEY"] = "TOKEN"
    
    # Token Auth
    geelark_app_token: str = ""
    
    # Key Auth
    geelark_app_id: str = ""
    geelark_api_key: str = ""
    
    # API Base URL
    geelark_api_base_url: str = "https://openapi.geelark.com/open/v1"
    
    # MultiLogin X
    multilogin_email: str = ""
    multilogin_password: str = ""
    multilogin_automation_token: str = ""
    multilogin_launcher_url: str = "https://launcher.mlx.yt:45001"
    
    # Database
    database_url: str = "sqlite:///./data/tiktok_automation.db"

    # AI Generation (Kie.ai for Nano Banana Pro + Kling/Hailuo)
    kie_api_key: str = ""

    # Optional: Anthropic for dynamic prompt variation (falls back to JSON templates if absent)
    anthropic_api_key: str = ""

    # App Settings
    log_level: str = "INFO"
    debug: bool = False

    # Automation Settings (TAP method)
    # warmup_days kept for legacy compatibility — TAP is lifecycle-driven via warmup_day field
    warmup_days: int = 7
    min_actions_per_day: int = 1   # TAP: 1-3 light actions max during early warmup
    max_actions_per_day: int = 3
    video_posts_per_day: int = 1   # Starts at 1, scales every 3 days, capped at 4
    min_delay_seconds: int = 30
    max_delay_seconds: int = 120
    
    # Video Storage — uses Render persistent disk if available
    video_storage_path: str = "/var/data/videos" if os.path.isdir("/var/data") else "./data/videos"
    
    def get_geelark_credentials(self) -> dict:
        """Return the appropriate credentials based on auth method."""
        if self.geelark_auth_method == "TOKEN":
            return {
                "method": "TOKEN",
                "token": self.geelark_app_token
            }
        else:
            return {
                "method": "KEY",
                "app_id": self.geelark_app_id,
                "api_key": self.geelark_api_key
            }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
