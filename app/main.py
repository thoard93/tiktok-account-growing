"""
TikTok Account Automation System
================================
FastAPI application for automating TikTok account growth using GeeLark cloud phones.

Features:
- Account creation with GeeLark cloud phones
- Proxy management (Proxiware integration)
- Progressive warmup automation
- Video upload and posting
- Activity logging and monitoring
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import get_settings
from app.database import init_db
from app.api.routes import router

settings = get_settings()

# Configure logging
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    # Startup
    logger.info("Starting TikTok Automation System...")
    
    # Ensure directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/videos", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Test GeeLark connection (optional)
    try:
        from app.services.geelark_client import GeeLarkClient
        creds = settings.get_geelark_credentials()
        if creds["method"] == "TOKEN" and creds["token"]:
            client = GeeLarkClient(
                base_url=settings.geelark_api_base_url,
                auth_method="TOKEN",
                app_token=creds["token"]
            )
            if client.test_connection():
                logger.info("GeeLark API connected successfully")
            else:
                logger.warning("GeeLark API connection failed - check credentials")
    except Exception as e:
        logger.warning(f"Could not test GeeLark connection: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down TikTok Automation System...")


# Create FastAPI app
app = FastAPI(
    title="TikTok Account Automation",
    description="Automate TikTok account growth using GeeLark cloud phones",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow dashboard access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "TikTok Account Automation System",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.debug
    )
