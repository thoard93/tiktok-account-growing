"""
Application Configuration
=========================
Manages environment variables and application settings.
"""

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
    
    # GeeLark Auth Method
    geelark_auth_method: Literal["TOKEN", "KEY"] = "TOKEN"
    
    # Token Auth
    geelark_app_token: str = ""
    
    # Key Auth
    geelark_app_id: str = ""
    geelark_api_key: str = ""
    
    # API Base URL
    geelark_api_base_url: str = "https://openapi.geelark.com/open/v1"
    
    # Database
    database_url: str = "sqlite:///./data/tiktok_automation.db"
    
    # App Settings
    log_level: str = "INFO"
    debug: bool = False
    
    # Automation Settings
    warmup_days: int = 5
    min_actions_per_day: int = 20
    max_actions_per_day: int = 50
    video_posts_per_day: int = 2
    min_delay_seconds: int = 30
    max_delay_seconds: int = 120
    
    # Video Storage
    video_storage_path: str = "./data/videos"
    
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
