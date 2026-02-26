"""
Phone Provider Abstraction Layer
==================================
Factory that returns the configured phone client (GeeLark or MultiLogin).

Usage:
    from app.services.phone_provider import get_phone_client
    client = get_phone_client()  # Returns GeeLarkClient or MultiLoginClient

The provider reads PHONE_PROVIDER env var to decide which client to return.
Both clients are used directly (not wrapped) — the service files reference
the client-specific methods they need.
"""

import os
from typing import Optional
from loguru import logger


# Cached singleton
_phone_client = None


def get_phone_client():
    """
    Get the configured phone client (GeeLark or MultiLogin).
    
    Reads PHONE_PROVIDER env var:
      - "multilogin" → MultiLoginClient
      - "geelark" (default) → GeeLarkClient
    
    Returns:
        GeeLarkClient or MultiLoginClient instance
    """
    global _phone_client
    
    if _phone_client is not None:
        return _phone_client
    
    provider = os.getenv("PHONE_PROVIDER", "geelark").lower().strip()
    
    if provider == "multilogin":
        from app.services.multilogin_client import MultiLoginClient
        _phone_client = MultiLoginClient()
        logger.info("Phone provider: MultiLogin X")
    else:
        from app.services.geelark_client import GeeLarkClient
        from app.config import get_settings
        settings = get_settings()
        creds = settings.get_geelark_credentials()
        
        if creds["method"] == "TOKEN":
            _phone_client = GeeLarkClient(
                base_url=settings.geelark_api_base_url,
                auth_method="TOKEN",
                app_token=creds["token"]
            )
        else:
            _phone_client = GeeLarkClient(
                base_url=settings.geelark_api_base_url,
                auth_method="KEY",
                app_id=creds["app_id"],
                api_key=creds["api_key"]
            )
        logger.info("Phone provider: GeeLark")
    
    return _phone_client


def reset_phone_client():
    """Reset the cached client (useful for testing or provider changes)."""
    global _phone_client
    _phone_client = None


def get_provider_name() -> str:
    """Get the current provider name."""
    return os.getenv("PHONE_PROVIDER", "geelark").lower().strip()


def is_multilogin() -> bool:
    """Check if the current provider is MultiLogin."""
    return get_provider_name() == "multilogin"
