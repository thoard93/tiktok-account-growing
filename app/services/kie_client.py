"""
Kie.ai API Client for AI Video Generation

Supports:
- Nano Banana Pro: Image generation (9:16 for TikTok)
- Grok Imagine: Image-to-video conversion (10s videos)
"""

import os
import httpx
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class KieTaskResult:
    """Result from a Kie.ai task"""
    success: bool
    task_id: Optional[str] = None
    result_urls: Optional[List[str]] = None
    error: Optional[str] = None
    state: Optional[str] = None


class KieClient:
    """
    Kie.ai API client for AI image and video generation.
    
    Models:
    - nano-banana-pro: Image generation ($0.09 for 1K)
    - grok-imagine/image-to-video: Video from image ($0.15 for 10s)
    """
    
    BASE_URL = "https://api.kie.ai/api/v1"
    
    # Model constants
    MODELS = {
        "IMAGE_GEN": "nano-banana-pro",
        "IMAGE_TO_VIDEO": "grok-imagine/image-to-video"
    }
    
    # Pricing (for cost tracking)
    COSTS = {
        "nano-banana-pro": 0.09,  # $0.09 per image (1K)
        "grok-imagine/image-to-video": 0.15  # $0.15 per 10s video
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Kie client with API key."""
        self.api_key = api_key or os.getenv("KIE_API_KEY")
        if not self.api_key:
            logger.warning("KIE_API_KEY not set - video generation will not work")
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make async request to Kie API."""
        url = f"{self.BASE_URL}{endpoint}"
        
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    def _make_request_sync(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make sync request to Kie API."""
        url = f"{self.BASE_URL}{endpoint}"
        
        with httpx.Client(timeout=60) as client:
            response = client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    # ===========================
    # Image Generation
    # ===========================
    
    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "9:16",  # TikTok vertical
        resolution: str = "1K",
        output_format: str = "png",
        callback_url: Optional[str] = None
    ) -> KieTaskResult:
        """
        Generate image using Nano Banana Pro.
        
        Args:
            prompt: Image description
            aspect_ratio: "9:16" for TikTok vertical
            resolution: "1K", "2K", or "4K"
            output_format: "png" or "jpg"
            callback_url: Optional webhook for completion
        
        Returns:
            KieTaskResult with task_id for polling
        """
        payload = {
            "model": self.MODELS["IMAGE_GEN"],
            "input": {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
                "output_format": output_format
            }
        }
        
        if callback_url:
            payload["callBackUrl"] = callback_url
        
        try:
            response = self._make_request_sync("/jobs/createTask", payload)
            
            if response.get("code") == 200:
                return KieTaskResult(
                    success=True,
                    task_id=response.get("data", {}).get("taskId"),
                    state="pending"
                )
            else:
                return KieTaskResult(
                    success=False,
                    error=response.get("message", "Unknown error")
                )
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return KieTaskResult(success=False, error=str(e))
    
    # ===========================
    # Image to Video
    # ===========================
    
    def image_to_video(
        self,
        image_url: str,
        prompt: str = "Smooth steady camera walking forward motion, natural movement",
        duration: str = "10",  # 10 seconds
        mode: str = "normal",  # normal, fun, or spicy
        callback_url: Optional[str] = None
    ) -> KieTaskResult:
        """
        Convert image to video using Grok Imagine.
        
        Args:
            image_url: URL of the source image
            prompt: Motion/action description
            duration: "6" or "10" seconds
            mode: "normal", "fun", or "spicy"
            callback_url: Optional webhook for completion
        
        Returns:
            KieTaskResult with task_id for polling
        """
        payload = {
            "model": self.MODELS["IMAGE_TO_VIDEO"],
            "input": {
                "image_urls": [image_url],
                "prompt": prompt,
                "mode": mode,
                "duration": duration
            }
        }
        
        if callback_url:
            payload["callBackUrl"] = callback_url
        
        try:
            response = self._make_request_sync("/jobs/createTask", payload)
            
            if response.get("code") == 200:
                return KieTaskResult(
                    success=True,
                    task_id=response.get("data", {}).get("taskId"),
                    state="pending"
                )
            else:
                return KieTaskResult(
                    success=False,
                    error=response.get("message", "Unknown error")
                )
        except Exception as e:
            logger.error(f"Image-to-video failed: {e}")
            return KieTaskResult(success=False, error=str(e))
    
    # ===========================
    # Task Status
    # ===========================
    
    def query_task(self, task_id: str) -> KieTaskResult:
        """
        Query task status.
        
        Args:
            task_id: Task ID from creation
        
        Returns:
            KieTaskResult with current state and result URLs if complete
        """
        payload = {"taskId": task_id}
        
        try:
            response = self._make_request_sync("/jobs/queryTask", payload)
            
            if response.get("code") == 200:
                data = response.get("data", {})
                state = data.get("state", "unknown")
                
                result_urls = None
                if state == "success":
                    result_json = data.get("resultJson", "{}")
                    if isinstance(result_json, str):
                        import json
                        result_data = json.loads(result_json)
                    else:
                        result_data = result_json
                    result_urls = result_data.get("resultUrls", [])
                
                return KieTaskResult(
                    success=state == "success",
                    task_id=task_id,
                    state=state,
                    result_urls=result_urls,
                    error=data.get("failMsg") if state == "fail" else None
                )
            else:
                return KieTaskResult(
                    success=False,
                    task_id=task_id,
                    error=response.get("message", "Query failed")
                )
        except Exception as e:
            logger.error(f"Task query failed: {e}")
            return KieTaskResult(success=False, task_id=task_id, error=str(e))
    
    def wait_for_task(
        self,
        task_id: str,
        timeout_seconds: int = 300,
        poll_interval: int = 5
    ) -> KieTaskResult:
        """
        Poll task until complete or timeout.
        
        Args:
            task_id: Task ID to wait for
            timeout_seconds: Max wait time
            poll_interval: Seconds between polls
        
        Returns:
            KieTaskResult with final state
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            result = self.query_task(task_id)
            
            if result.state in ["success", "fail"]:
                return result
            
            logger.info(f"Task {task_id} state: {result.state}, waiting...")
            time.sleep(poll_interval)
        
        return KieTaskResult(
            success=False,
            task_id=task_id,
            state="timeout",
            error=f"Task timed out after {timeout_seconds}s"
        )


# Singleton instance
_kie_client: Optional[KieClient] = None

def get_kie_client() -> KieClient:
    """Get or create Kie client singleton."""
    global _kie_client
    if _kie_client is None:
        _kie_client = KieClient()
    return _kie_client
