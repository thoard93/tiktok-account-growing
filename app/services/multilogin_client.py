"""
MultiLogin X API Client
========================
Wrapper for MultiLogin X API for cloud Android phone management.

API Docs: https://documenter.getpostman.com/view/28533318/2s946h9Cv0
Management API: https://api.multilogin.com
Launcher API: https://launcher.mlx.yt:45001 (requires desktop app running)

Authentication: Email + MD5-hashed password → Bearer token (30min TTL, auto-refresh)
Alternative: Workspace Automation Token (permanent, higher rate limits)

Mobile profiles use os_type="android" with the same endpoints as browser profiles.
"""

import os
import time
import hashlib
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from loguru import logger
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class MultiLoginResponse:
    """Standardized response from MultiLogin API."""
    success: bool
    status_code: int = 0
    message: str = ""
    data: Any = None


@dataclass
class MultiLoginProfile:
    """Represents a MultiLogin mobile profile (cloud phone)."""
    profile_id: str = ""
    name: str = ""
    os_type: str = ""
    status: str = ""  # "new", "running", "stopped"
    folder_id: str = ""
    storage_type: str = ""
    created_at: str = ""
    tags: List[str] = field(default_factory=list)


class MultiLoginClient:
    """
    MultiLogin X API Client for cloud Android phone management.
    
    Mirrors the GeeLarkClient interface for easy swapping.
    
    Two API surfaces:
    - Management API (api.multilogin.com): Profile CRUD, auth, proxy
    - Launcher API (launcher.mlx.yt:45001): Start/stop/status (requires desktop app)
    
    Auth methods:
    - Email + Password: Auto-generates bearer token, refreshes every 25min
    - Automation Token: Permanent token from dashboard settings (recommended)
    """
    
    MANAGEMENT_URL = "https://api.multilogin.com"
    LAUNCHER_URL = "https://launcher.mlx.yt:45001"
    
    # Default folder ID (you can override per-call)
    DEFAULT_FOLDER_ID = "0"  # Root folder
    
    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        automation_token: Optional[str] = None,
        launcher_url: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize MultiLogin X client.
        
        Args:
            email: Account email (for password auth)
            password: Account password (will be MD5 hashed)
            automation_token: Permanent automation token (from dashboard)
            launcher_url: Override launcher URL (default: https://launcher.mlx.yt:45001)
            max_retries: Number of retries on failure
            timeout: Request timeout in seconds
        """
        self.email = email or os.getenv("MULTILOGIN_EMAIL")
        self.password = password or os.getenv("MULTILOGIN_PASSWORD")
        self.automation_token = automation_token or os.getenv("MULTILOGIN_AUTOMATION_TOKEN")
        self.launcher_url = (launcher_url or os.getenv("MULTILOGIN_LAUNCHER_URL", self.LAUNCHER_URL)).rstrip("/")
        self.timeout = timeout
        
        # Token state
        self._bearer_token: Optional[str] = None
        self._refresh_token_value: Optional[str] = None
        self._token_expires_at: float = 0
        
        # Validate auth
        if not self.automation_token and not (self.email and self.password):
            logger.warning(
                "MultiLogin: No credentials provided. "
                "Set MULTILOGIN_AUTOMATION_TOKEN or MULTILOGIN_EMAIL + MULTILOGIN_PASSWORD"
            )
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Auto-authenticate if credentials provided
        if self.automation_token:
            self._bearer_token = self.automation_token
            self._token_expires_at = float("inf")  # Permanent token
            logger.info("MultiLogin client initialized with automation token")
        elif self.email and self.password:
            self._authenticate()
            logger.info(f"MultiLogin client initialized with email auth ({self.email})")
        else:
            logger.warning("MultiLogin client initialized without credentials")
    
    # ===========================
    # Authentication
    # ===========================
    
    def _md5_hash(self, text: str) -> str:
        """MD5 hash a string (required for password auth)."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _authenticate(self) -> bool:
        """Sign in with email + MD5-hashed password to get bearer token."""
        try:
            response = self.session.post(
                f"{self.MANAGEMENT_URL}/user/signin",
                json={
                    "email": self.email,
                    "password": self._md5_hash(self.password)
                },
                timeout=self.timeout
            )
            
            result = response.json()
            
            if response.status_code == 200 and result.get("data", {}).get("token"):
                self._bearer_token = result["data"]["token"]
                self._refresh_token_value = result["data"].get("refresh_token")
                # Token expires in 30 min, refresh at 25 min
                self._token_expires_at = time.time() + (25 * 60)
                logger.info("MultiLogin: Authentication successful")
                return True
            else:
                logger.error(f"MultiLogin auth failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"MultiLogin auth error: {e}")
            return False
    
    def _refresh_token(self) -> bool:
        """Refresh the bearer token before it expires."""
        if not self._refresh_token_value:
            return self._authenticate()
        
        try:
            response = self.session.post(
                f"{self.MANAGEMENT_URL}/user/refresh_token",
                json={"refresh_token": self._refresh_token_value},
                timeout=self.timeout
            )
            
            result = response.json()
            
            if response.status_code == 200 and result.get("data", {}).get("token"):
                self._bearer_token = result["data"]["token"]
                self._refresh_token_value = result["data"].get("refresh_token", self._refresh_token_value)
                self._token_expires_at = time.time() + (25 * 60)
                logger.debug("MultiLogin: Token refreshed")
                return True
            else:
                logger.warning("MultiLogin: Token refresh failed, re-authenticating...")
                return self._authenticate()
                
        except Exception as e:
            logger.error(f"MultiLogin token refresh error: {e}")
            return self._authenticate()
    
    def _ensure_token(self):
        """Ensure we have a valid bearer token, refreshing if needed."""
        if time.time() >= self._token_expires_at:
            self._refresh_token()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers."""
        self._ensure_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._bearer_token}"
        }
    
    # ===========================
    # Core Request Methods
    # ===========================
    
    def _management_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> MultiLoginResponse:
        """
        Make authenticated request to Management API (api.multilogin.com).
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API path (e.g., "/profile/create")
            data: JSON body for POST/PUT
            params: Query params for GET
            
        Returns:
            MultiLoginResponse with parsed result
        """
        url = f"{self.MANAGEMENT_URL}{endpoint}"
        headers = self._get_headers()
        
        logger.debug(f"MultiLogin API: {method} {endpoint}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            result = response.json() if response.text else {}
            status = response.status_code
            
            # MultiLogin returns 200/201 on success
            success = status in [200, 201]
            
            if not success:
                msg = result.get("message", result.get("error", f"HTTP {status}"))
                logger.warning(f"MultiLogin API Error: {endpoint} → {msg} (HTTP {status})")
                logger.warning(f"MultiLogin API Error Body: {result}")
                if data:
                    logger.warning(f"MultiLogin API Request Payload: {data}")
                return MultiLoginResponse(
                    success=False,
                    status_code=status,
                    message=msg,
                    data=result
                )
            
            return MultiLoginResponse(
                success=True,
                status_code=status,
                message="OK",
                data=result.get("data", result)
            )
            
        except requests.exceptions.Timeout:
            logger.error(f"MultiLogin API Timeout: {endpoint}")
            return MultiLoginResponse(success=False, status_code=0, message="Request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"MultiLogin API Error: {e}")
            return MultiLoginResponse(success=False, status_code=0, message=str(e))
        except Exception as e:
            logger.error(f"MultiLogin unexpected error: {e}")
            return MultiLoginResponse(success=False, status_code=0, message=str(e))
    
    def _launcher_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> MultiLoginResponse:
        """
        Make request to Launcher API (launcher.mlx.yt:45001).
        Requires MultiLogin X desktop app running.
        
        Args:
            method: HTTP method
            endpoint: API path
            params: Query parameters
            data: JSON body
            
        Returns:
            MultiLoginResponse
        """
        url = f"{self.launcher_url}{endpoint}"
        headers = self._get_headers()
        
        logger.debug(f"MultiLogin Launcher: {method} {endpoint}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            result = response.json() if response.text else {}
            status = response.status_code
            success = status in [200, 201]
            
            if not success:
                msg = result.get("message", result.get("error", f"HTTP {status}"))
                logger.warning(f"MultiLogin Launcher Error: {endpoint} → {msg}")
                return MultiLoginResponse(success=False, status_code=status, message=msg, data=result)
            
            return MultiLoginResponse(
                success=True,
                status_code=status,
                message="OK",
                data=result.get("data", result)
            )
            
        except requests.exceptions.ConnectionError:
            logger.error(
                "MultiLogin Launcher not reachable. "
                "Is the MultiLogin X desktop app running?"
            )
            return MultiLoginResponse(
                success=False, status_code=0,
                message="Launcher not reachable - is MultiLogin X desktop app running?"
            )
        except Exception as e:
            logger.error(f"MultiLogin Launcher error: {e}")
            return MultiLoginResponse(success=False, status_code=0, message=str(e))
    
    # ===========================
    # Profile Management (CRUD)
    # ===========================
    
    def create_phone(
        self,
        name: str,
        os_version: str = "Android 12",
        storage_type: str = "cloud",
        folder_id: Optional[str] = None,
        proxy_type: Optional[str] = None,
        proxy_host: Optional[str] = None,
        proxy_port: Optional[int] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        use_multilogin_proxy: bool = True,
        proxy_country: str = "us",
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None
    ) -> MultiLoginResponse:
        """
        Create a new mobile profile (cloud phone).
        
        Equivalent to GeeLarkClient.create_single_phone().
        
        Args:
            name: Profile name (max 100 chars)
            os_version: Android version (e.g., "Android 12")
            storage_type: "cloud" or "local"
            folder_id: Folder to place profile in
            proxy_type: "http", "socks5" (ignored if use_multilogin_proxy=True)
            proxy_host: Proxy hostname/IP
            proxy_port: Proxy port
            proxy_username: Proxy username
            proxy_password: Proxy password
            use_multilogin_proxy: Use built-in MultiLogin residential proxy
            proxy_country: Country code for built-in proxy (e.g., "us")
            tags: List of tag names
            notes: Profile notes
            
        Returns:
            MultiLoginResponse with profile_id in data
        """
        payload = {
            "name": name[:100],
            "os_type": "android",
            "browser_type": "mimic",
            "storage_type": storage_type,
            "folder_id": folder_id or self.DEFAULT_FOLDER_ID,
        }
        
        # Proxy configuration
        if use_multilogin_proxy:
            payload["parameters"] = {
                "proxy": {
                    "type": "multilogin",
                    "country": proxy_country
                }
            }
        elif proxy_host:
            payload["parameters"] = {
                "proxy": {
                    "type": proxy_type or "http",
                    "host": proxy_host,
                    "port": proxy_port,
                    "username": proxy_username or "",
                    "password": proxy_password or ""
                }
            }
        
        if tags:
            payload["tags"] = tags
        if notes:
            payload["notes"] = notes
        
        result = self._management_request("POST", "/profile/create", payload)
        
        if result.success:
            profile_id = result.data.get("ids", [None])[0] if isinstance(result.data, dict) else None
            if not profile_id and isinstance(result.data, dict):
                profile_id = result.data.get("id")
            logger.info(f"MultiLogin: Created phone '{name}' → {profile_id}")
            result.data = {"profile_id": profile_id, "raw": result.data}
        
        return result
    
    def create_phones_batch(
        self,
        names: List[str],
        **kwargs
    ) -> List[MultiLoginResponse]:
        """
        Create multiple phones (convenience wrapper).
        
        Args:
            names: List of phone names
            **kwargs: Passed to create_phone()
            
        Returns:
            List of MultiLoginResponse results
        """
        results = []
        for name in names:
            result = self.create_phone(name=name, **kwargs)
            results.append(result)
            time.sleep(0.5)  # Rate limit safety
        return results
    
    def list_phones(
        self,
        search_text: Optional[str] = None,
        offset: int = 0,
        limit: int = 50,
        storage_type: str = "all",
        folder_id: Optional[str] = None
    ) -> MultiLoginResponse:
        """
        List/search mobile profiles.
        
        Equivalent to GeeLarkClient.list_phones().
        
        Args:
            search_text: Filter by name
            offset: Pagination offset
            limit: Max results (1-100)
            storage_type: "cloud", "local", or "all"
            folder_id: Filter by folder
            
        Returns:
            MultiLoginResponse with list of profiles
        """
        payload = {
            "search_text": search_text or "",
            "limit": min(limit, 100),
            "offset": offset
        }
        
        if storage_type and storage_type != "all":
            payload["storage_type"] = storage_type
        if folder_id:
            payload["folder_id"] = folder_id
        
        return self._management_request("POST", "/profile/search", payload)
    
    def get_phone_status(self, profile_id: str) -> MultiLoginResponse:
        """
        Get status of a single mobile profile.
        
        Equivalent to GeeLarkClient.get_phone_status().
        
        Args:
            profile_id: Profile ID
            
        Returns:
            MultiLoginResponse with status ("new", "running", "stopped", etc.)
        """
        return self._launcher_request(
            "GET",
            f"/api/v1/profile/status/p/{profile_id}"
        )
    
    def delete_phones(self, profile_ids: List[str]) -> MultiLoginResponse:
        """
        Delete mobile profiles.
        
        Equivalent to GeeLarkClient.delete_phones().
        
        Args:
            profile_ids: List of profile IDs to delete
            
        Returns:
            MultiLoginResponse
        """
        return self._management_request(
            "POST",
            "/profile/remove",
            {"ids": profile_ids}
        )
    
    # ===========================
    # Launcher (Start/Stop)
    # ===========================
    
    def start_phones(
        self,
        profile_ids: List[str],
        folder_id: Optional[str] = None,
        automation_type: str = "selenium"
    ) -> MultiLoginResponse:
        """
        Start mobile profiles (cloud phones).
        
        Equivalent to GeeLarkClient.start_phones().
        Requires MultiLogin X desktop app running.
        
        Args:
            profile_ids: List of profile IDs to start
            folder_id: Folder ID (default: root)
            automation_type: "selenium", "puppeteer", or "playwright"
            
        Returns:
            MultiLoginResponse with port info for each started profile
        """
        folder = folder_id or self.DEFAULT_FOLDER_ID
        results = []
        
        for pid in profile_ids:
            result = self._launcher_request(
                "GET",
                f"/api/v2/profile/f/{folder}/p/{pid}/start",
                params={"automation_type": automation_type}
            )
            results.append({
                "profile_id": pid,
                "success": result.success,
                "port": result.data.get("port") if result.success and isinstance(result.data, dict) else None,
                "message": result.message
            })
            
            if result.success:
                logger.info(f"MultiLogin: Started phone {pid} (port: {results[-1]['port']})")
            else:
                logger.error(f"MultiLogin: Failed to start phone {pid}: {result.message}")
            
            # Small delay between starts
            if len(profile_ids) > 1:
                time.sleep(1)
        
        success_count = sum(1 for r in results if r["success"])
        
        return MultiLoginResponse(
            success=success_count > 0,
            status_code=200 if success_count > 0 else 500,
            message=f"Started {success_count}/{len(profile_ids)} phones",
            data={
                "totalAmount": len(profile_ids),
                "successAmount": success_count,
                "failAmount": len(profile_ids) - success_count,
                "details": results
            }
        )
    
    def stop_phones(self, profile_ids: List[str]) -> MultiLoginResponse:
        """
        Stop mobile profiles.
        
        Equivalent to GeeLarkClient.stop_phones().
        
        Args:
            profile_ids: List of profile IDs to stop
            
        Returns:
            MultiLoginResponse
        """
        results = []
        
        for pid in profile_ids:
            result = self._launcher_request(
                "GET",
                "/api/v1/profile/stop",
                params={"profile_id": pid}
            )
            results.append({
                "profile_id": pid,
                "success": result.success,
                "message": result.message
            })
        
        success_count = sum(1 for r in results if r["success"])
        
        return MultiLoginResponse(
            success=success_count > 0,
            status_code=200,
            message=f"Stopped {success_count}/{len(profile_ids)} phones",
            data={
                "totalAmount": len(profile_ids),
                "successAmount": success_count,
                "failAmount": len(profile_ids) - success_count,
                "details": results
            }
        )
    
    def stop_all_phones(self) -> MultiLoginResponse:
        """Stop all running profiles."""
        return self._launcher_request("GET", "/api/v1/profile/stop/all")
    
    # ===========================
    # File Upload (Object Storage)
    # ===========================
    
    def upload_video_to_phone(
        self,
        profile_id: str,
        local_file_path: str
    ) -> MultiLoginResponse:
        """
        Upload a video file to a cloud phone's storage.
        
        Equivalent to GeeLarkClient.upload_video_to_phone().
        Uses Object Storage API.
        
        Args:
            profile_id: Profile ID
            local_file_path: Path to local video file
            
        Returns:
            MultiLoginResponse
        """
        import os as _os
        
        if not _os.path.exists(local_file_path):
            return MultiLoginResponse(
                success=False, message=f"File not found: {local_file_path}"
            )
        
        try:
            # Upload to Object Storage
            with open(local_file_path, "rb") as f:
                filename = _os.path.basename(local_file_path)
                
                # MultiLogin Object Storage upload
                headers = self._get_headers()
                headers.pop("Content-Type", None)  # Let requests set multipart boundary
                
                response = self.session.post(
                    f"{self.MANAGEMENT_URL}/profile/upload_object",
                    files={"file": (filename, f)},
                    data={"profile_id": profile_id},
                    headers=headers,
                    timeout=120
                )
                
                if response.status_code in [200, 201]:
                    logger.info(f"MultiLogin: Uploaded {filename} to phone {profile_id}")
                    return MultiLoginResponse(
                        success=True,
                        status_code=response.status_code,
                        message="Upload successful",
                        data=response.json() if response.text else {}
                    )
                else:
                    return MultiLoginResponse(
                        success=False,
                        status_code=response.status_code,
                        message=f"Upload failed: {response.text}"
                    )
                    
        except Exception as e:
            logger.error(f"MultiLogin upload error: {e}")
            return MultiLoginResponse(success=False, message=str(e))
    
    # ===========================
    # Proxy Management
    # ===========================
    
    def generate_proxy(
        self,
        country: str = "us",
        session_type: str = "sticky",
        protocol: str = "http"
    ) -> MultiLoginResponse:
        """
        Generate a MultiLogin built-in proxy connection URL.
        
        Args:
            country: Country code (e.g., "us", "gb", "de")
            session_type: "sticky" or "rotating"
            protocol: "http" or "socks5"
            
        Returns:
            MultiLoginResponse with proxy connection URL
        """
        return self._management_request(
            "POST",
            "https://profile-proxy.multilogin.com/v1/proxy/connection_url",
            {
                "country": country,
                "sessionType": session_type,
                "protocol": protocol
            }
        )
    
    # ===========================
    # Connection Testing
    # ===========================
    
    def test_connection(self) -> MultiLoginResponse:
        """
        Test connection to both Management and Launcher APIs.
        
        Returns:
            MultiLoginResponse with connection status for both APIs
        """
        management_ok = False
        launcher_ok = False
        
        # Test management API
        try:
            response = self.session.get(
                f"{self.MANAGEMENT_URL}/user/me",
                headers=self._get_headers(),
                timeout=10
            )
            management_ok = response.status_code == 200
        except Exception as e:
            logger.warning(f"Management API test failed: {e}")
        
        # Test launcher API
        try:
            response = self.session.get(
                f"{self.launcher_url}/api/v1/profile/stop/all",
                headers=self._get_headers(),
                timeout=5
            )
            launcher_ok = response.status_code in [200, 404]  # 404 = no profiles running, but reachable
        except Exception:
            logger.warning("Launcher API not reachable (is desktop app running?)")
        
        return MultiLoginResponse(
            success=management_ok,
            message=(
                f"Management API: {'✓' if management_ok else '✗'} | "
                f"Launcher API: {'✓' if launcher_ok else '✗ (desktop app needed)'}"
            ),
            data={
                "management_api": management_ok,
                "launcher_api": launcher_ok
            }
        )


# ===========================
# Singleton & Factory
# ===========================

_multilogin_client: Optional[MultiLoginClient] = None


def get_multilogin_client() -> MultiLoginClient:
    """Get or create MultiLogin client singleton."""
    global _multilogin_client
    if _multilogin_client is None:
        _multilogin_client = MultiLoginClient()
    return _multilogin_client
