"""
GeeLark API Client
==================
Wrapper for GeeLark Open API with both Token and Key authentication methods.

API Docs: https://open.geelark.com/api
Base URL: https://openapi.geelark.com/open/v1

Endpoints documented from official API:
- /phone/list - Get all cloud phones
- /phone/addNew - Create new cloud phones (V2 API)
- /phone/start - Batch start cloud phones
- /phone/stop - Stop cloud phones
- /task/query - Query task status
"""

import uuid
import time
import hashlib
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from loguru import logger
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class GeeLarkResponse:
    """Standardized response from GeeLark API."""
    success: bool
    code: int
    message: str
    data: Any
    trace_id: str


class GeeLarkClient:
    """
    GeeLark Open API Client
    
    Supports both authentication methods:
    - TOKEN: Bearer token (simpler, for personal use)
    - KEY: App ID + API Key with signature (more secure, for production)
    
    Rate Limits: 200 req/min, 24,000 req/hour
    """
    
    # Official API Endpoints
    ENDPOINTS = {
        # Phone Management
        "phone_list": "/phone/list",
        "phone_add_new": "/phone/addNew",  # V2 API
        "phone_start": "/phone/start",
        "phone_stop": "/phone/stop",
        "phone_delete": "/phone/delete",
        "phone_status": "/phone/status",
        "phone_detail_update": "/phone/detail/update",
        "phone_new_one": "/v2/phone/newOne",  # One-click new machine V2
        "phone_serial_num": "/phone/serialNum/get",  # Get device ID
        
        # Task Management
        "task_query": "/task/query",
        "task_add": "/task/add",
        "task_history": "/task/historyRecords",
        "task_cancel": "/task/cancel",
        "task_restart": "/task/restart",
        "task_detail": "/task/detail",
        
        # Proxy Management
        "proxy_add": "/proxy/add",
        "proxy_update": "/proxy/update",
        "proxy_delete": "/proxy/delete",
        "proxy_list": "/proxy/list",
        
        # App Management  
        "app_list": "/app/list",
        "app_install": "/app/install",
        "app_start": "/app/start",
        "app_stop": "/app/stop",
        "app_uninstall": "/app/uninstall",
        "app_upload": "/app/upload",
        "app_upload_status": "/app/upload/status",
        "app_shop_list": "/app/shop/list",
        "app_add": "/app/add",
        "app_team_list": "/app/teamApp/list",
        "app_remove": "/app/remove",
        "app_operation_batch": "/app/operation/batch",
        "app_set_keep_alive": "/app/setKeepAlive",
        
        # RPA/Automation
        "rpa_tiktok_warmup": "/rpa/tiktok/warmup",
        "rpa_tiktok_post": "/rpa/tiktok/post",
        "rpa_tiktok_login": "/rpa/tiktok/login",
        
        # File Management
        "upload_get_url": "/upload/getUrl",  # Get temp upload URL
        "phone_upload_file": "/phone/uploadFile",  # Upload file to phone
        "phone_upload_file_result": "/phone/uploadFile/result",  # Query upload status
        "keybox_upload": "/phone/keyboxUpload",
        "keybox_upload_result": "/phone/keyboxUpload/result",
        
        # ADB Management
        "adb_set_status": "/adb/setStatus",
        "adb_get_data": "/adb/getData",
    }
    
    # Task Type Constants (from API docs)
    TASK_TYPES = {
        "TIKTOK_VIDEO_POSTING": 1,
        "TIKTOK_AI_WARMUP": 2,
        "TIKTOK_CAROUSEL_POSTING": 3,
        "TIKTOK_ACCOUNT_LOGIN": 4,
        "TIKTOK_PROFILE_EDITING": 6,
        "CUSTOM": 42,
    }
    
    # Task Status Constants
    TASK_STATUS = {
        1: "waiting",
        2: "in_progress",
        3: "completed",
        4: "failed",
        7: "cancelled",
    }
    
    def __init__(
        self,
        base_url: str = "https://openapi.geelark.com/open/v1",
        auth_method: str = "TOKEN",
        app_token: Optional[str] = None,
        app_id: Optional[str] = None,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize GeeLark API client.
        
        Args:
            base_url: API base URL
            auth_method: "TOKEN" or "KEY"
            app_token: Bearer token for TOKEN auth
            app_id: App ID for KEY auth
            api_key: API Key for KEY auth
            max_retries: Number of retries on failure
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.auth_method = auth_method.upper()
        self.app_token = app_token
        self.app_id = app_id
        self.api_key = api_key
        self.timeout = timeout
        
        # Validate auth credentials
        if self.auth_method == "TOKEN" and not self.app_token:
            raise ValueError("app_token required for TOKEN auth method")
        if self.auth_method == "KEY" and (not self.app_id or not self.api_key):
            raise ValueError("app_id and api_key required for KEY auth method")
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        logger.info(f"GeeLark client initialized with {self.auth_method} auth")
    
    def _generate_trace_id(self) -> str:
        """Generate UUID v4 for request tracing."""
        return str(uuid.uuid4()).upper()
    
    def _generate_key_auth_headers(self, trace_id: str) -> Dict[str, str]:
        """
        Generate headers for KEY authentication method.
        
        Sign format: SHA256(appId + traceId + ts + nonce + apiKey).toUpperCase()
        """
        timestamp = str(int(time.time() * 1000))
        nonce = trace_id[:6]
        
        # Create signature
        sign_string = f"{self.app_id}{trace_id}{timestamp}{nonce}{self.api_key}"
        sign = hashlib.sha256(sign_string.encode()).hexdigest().upper()
        
        return {
            "Content-Type": "application/json",
            "appId": self.app_id,
            "traceId": trace_id,
            "ts": timestamp,
            "nonce": nonce,
            "sign": sign
        }
    
    def _generate_token_auth_headers(self, trace_id: str) -> Dict[str, str]:
        """Generate headers for TOKEN authentication method."""
        return {
            "Content-Type": "application/json",
            "traceId": trace_id,
            "Authorization": f"Bearer {self.app_token}"
        }
    
    def _get_headers(self, trace_id: str) -> Dict[str, str]:
        """Get appropriate headers based on auth method."""
        if self.auth_method == "KEY":
            return self._generate_key_auth_headers(trace_id)
        return self._generate_token_auth_headers(trace_id)
    
    def _make_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> GeeLarkResponse:
        """
        Make authenticated POST request to GeeLark API.
        
        Args:
            endpoint: API endpoint path (without base URL)
            data: Request body data
            
        Returns:
            GeeLarkResponse with parsed response
        """
        trace_id = self._generate_trace_id()
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(trace_id)
        
        logger.debug(f"GeeLark API Request: {endpoint} | TraceID: {trace_id}")
        
        try:
            response = self.session.post(
                url,
                json=data or {},
                headers=headers,
                timeout=self.timeout
            )
            
            # Parse response
            result = response.json()
            code = result.get("code", -1)
            success = code == 0
            
            geelark_response = GeeLarkResponse(
                success=success,
                code=code,
                message=result.get("msg", ""),
                data=result.get("data"),
                trace_id=result.get("traceId", trace_id)
            )
            
            if not success:
                logger.warning(
                    f"GeeLark API Error: {geelark_response.message} "
                    f"(code: {code}, traceId: {trace_id})"
                )
            
            return geelark_response
            
        except requests.exceptions.Timeout:
            logger.error(f"GeeLark API Timeout: {endpoint}")
            return GeeLarkResponse(
                success=False,
                code=-1,
                message="Request timeout",
                data=None,
                trace_id=trace_id
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"GeeLark API Error: {e}")
            return GeeLarkResponse(
                success=False,
                code=-1,
                message=str(e),
                data=None,
                trace_id=trace_id
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return GeeLarkResponse(
                success=False,
                code=-1,
                message=str(e),
                data=None,
                trace_id=trace_id
            )
    
    # ===========================
    # Phone Management Methods
    # ===========================
    
    def list_phones(
        self,
        page: int = 1,
        page_size: int = 20,
        ids: Optional[List[str]] = None,
        serial_name: Optional[str] = None,
        group_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        open_status: Optional[int] = None,
        charge_mode: Optional[int] = None
    ) -> GeeLarkResponse:
        """
        Get all cloud phones with optional filtering.
        
        Args:
            page: Page number (min 1)
            page_size: Items per page (1-100)
            ids: Filter by specific phone IDs (max 100, ignores pagination)
            serial_name: Filter by phone name
            group_name: Filter by group name
            tags: Filter by tags
            open_status: 0=closed, 1=on
            charge_mode: 0=pay per minute, 1=monthly subscription
        """
        data = {
            "page": page,
            "pageSize": min(page_size, 100)
        }
        
        if ids:
            data["ids"] = ids[:100]
        if serial_name:
            data["serialName"] = serial_name
        if group_name:
            data["groupName"] = group_name
        if tags:
            data["tags"] = tags
        if open_status is not None:
            data["openStatus"] = open_status
        if charge_mode is not None:
            data["chargeMode"] = charge_mode
            
        return self._make_request(self.ENDPOINTS["phone_list"], data)
    
    def create_phones(
        self,
        profiles: List[Dict[str, Any]],
        mobile_type: str = "Android 12",
        charge_mode: int = 0,
        region: str = "cn"
    ) -> GeeLarkResponse:
        """
        Create new cloud phones using V2 API (addNew).
        
        Args:
            profiles: List of profile configs, each containing:
                - profileName (required): Cloud phone name
                - proxyInformation: Proxy string (e.g., "socks5://user:pass@ip:port")
                - refreshUrl: Proxy refresh URL
                - dynamicProxy: Dynamic proxy provider name
                - dynamicProxyLocation: Dynamic proxy country code
                - mobileRegion: Phone region (e.g., "USA-US")
                - mobileProvince: State (US only)
                - mobileCity: City (US only)
                - mobileLanguage: Language code or "default"
                - profileGroup: Group name (auto-created if doesn't exist)
                - profileTags: List of tag names
                - profileNote: Remark
                - surfaceBrandName: Phone brand
                - surfaceModelName: Phone model
                - netType: 0=Wi-Fi, 1=Mobile
                - phoneNumber: Phone number (auto-generated if empty)
            mobile_type: Android version (9, 10, 11, 12, 13, 14, 15)
            charge_mode: 0=on-demand, 1=monthly
            region: Server region (cn, sgp)
        """
        data = {
            "mobileType": mobile_type,
            "chargeMode": charge_mode,
            "region": region,
            "data": profiles
        }
        
        return self._make_request(self.ENDPOINTS["phone_add_new"], data)
    
    def create_single_phone(
        self,
        name: str,
        proxy_string: Optional[str] = None,
        mobile_type: str = "Android 12",
        group: Optional[str] = None,
        tags: Optional[List[str]] = None,
        region: str = "USA-US",
        language: str = "default"
    ) -> GeeLarkResponse:
        """
        Helper to create a single cloud phone.
        
        Args:
            name: Phone name
            proxy_string: Proxy in format "protocol://user:pass@host:port"
            mobile_type: Android version
            group: Group name
            tags: Tag names
            region: Mobile region code
            language: Language or "default"
        """
        profile = {
            "profileName": name,
            "mobileRegion": region,
            "mobileLanguage": language
        }
        
        if proxy_string:
            profile["proxyInformation"] = proxy_string
        if group:
            profile["profileGroup"] = group
        if tags:
            profile["profileTags"] = tags
        
        return self.create_phones(
            profiles=[profile],
            mobile_type=mobile_type
        )
    
    def start_phones(
        self,
        ids: List[str],
        width: int = 336,
        center: int = 1,
        energy_saving_mode: int = 0
    ) -> GeeLarkResponse:
        """
        Batch start cloud phones.
        
        Args:
            ids: List of cloud phone IDs to start
            width: Display width in px (200-600, default 336)
            center: 0=not centered, 1=centered
            energy_saving_mode: 0=disabled, 1=enabled (auto-shutdown after 30min idle)
            
        Returns:
            Response with totalAmount, successAmount, failAmount, and details
        """
        data = {
            "ids": ids,
            "width": width,
            "center": center,
            "energySavingMode": energy_saving_mode
        }
        
        return self._make_request(self.ENDPOINTS["phone_start"], data)
    
    def stop_phones(self, ids: List[str]) -> GeeLarkResponse:
        """
        Stop cloud phones.
        
        Args:
            ids: List of cloud phone IDs to stop
        """
        return self._make_request(self.ENDPOINTS["phone_stop"], {"ids": ids})
    
    def delete_phones(self, ids: List[str]) -> GeeLarkResponse:
        """
        Delete cloud phones.
        
        Args:
            ids: List of cloud phone IDs to delete
        """
        return self._make_request(self.ENDPOINTS["phone_delete"], {"ids": ids})
    
    def get_phone_status(self, ids: List[str]) -> GeeLarkResponse:
        """
        Get status of cloud phones.
        
        Args:
            ids: List of cloud phone IDs (max 100)
            
        Returns:
            Response with status codes:
            0 - Started
            1 - Starting
            2 - Shut down
            3 - Expired
        """
        return self._make_request(self.ENDPOINTS["phone_status"], {"ids": ids[:100]})
    
    def update_phone(
        self,
        phone_id: str,
        name: Optional[str] = None,
        remark: Optional[str] = None,
        group_id: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        proxy_config: Optional[Dict[str, Any]] = None,
        proxy_id: Optional[str] = None,
        phone_number: Optional[str] = None
    ) -> GeeLarkResponse:
        """
        Update cloud phone information.
        Warning: Do not call while starting the cloud phone.
        
        Args:
            phone_id: Cloud phone ID
            name: New name (max 100 chars)
            remark: New remark (max 1500 chars)
            group_id: New group ID
            tag_ids: New tag IDs
            proxy_config: New proxy config (typeId, server, port, username, password)
            proxy_id: Proxy ID
            phone_number: Custom phone number (requires shutdown state)
        """
        data = {"id": phone_id}
        
        if name:
            data["name"] = name
        if remark:
            data["remark"] = remark
        if group_id:
            data["groupID"] = group_id
        if tag_ids:
            data["tagIDs"] = tag_ids
        if proxy_config:
            data["proxyConfig"] = proxy_config
        if proxy_id:
            data["proxyId"] = proxy_id
        if phone_number:
            data["phoneNumber"] = phone_number
            
        return self._make_request(self.ENDPOINTS["phone_detail_update"], data)
    
    def one_click_new_machine(
        self,
        phone_id: str,
        change_brand_model: bool = True,
        keep_net_type: bool = False,
        keep_phone_number: bool = False,
        keep_region: bool = False,
        keep_language: bool = False
    ) -> GeeLarkResponse:
        """
        One-click new machine - reset phone identity.
        
        Args:
            phone_id: Cloud phone ID
            change_brand_model: Randomize brand/model (True) or keep (False)
            keep_net_type: Preserve network connection type
            keep_phone_number: Preserve phone number
            keep_region: Preserve region (False = follow proxy)
            keep_language: Preserve language (False = use English)
        """
        data = {
            "id": phone_id,
            "changeBrandModel": change_brand_model,
            "keepNetType": keep_net_type,
            "keepPhoneNumber": keep_phone_number,
            "keepRegion": keep_region,
            "keepLanguage": keep_language
        }
        return self._make_request(self.ENDPOINTS["phone_new_one"], data)
    
    def get_device_id(self, phone_id: str) -> GeeLarkResponse:
        """
        Get the cloud phone device ID (Android ID equivalent).
        Re-obtain after one-click new phone to get latest ID.
        
        Args:
            phone_id: Cloud phone ID
            
        Returns:
            Response with serialNum (device ID)
        """
        return self._make_request(self.ENDPOINTS["phone_serial_num"], {"id": phone_id})
    
    # ===========================
    # Proxy Management Methods
    # ===========================
    
    def add_proxies(
        self,
        proxies: List[Dict[str, Any]]
    ) -> GeeLarkResponse:
        """
        Add proxies to GeeLark (duplicates not added).
        
        Args:
            proxies: List of proxy configs (max 100), each with:
                - scheme: "socks5", "http", or "https"
                - server: Proxy address
                - port: Proxy port
                - username: (optional)
                - password: (optional)
                
        Returns:
            Response with success/fail details and proxy IDs
        """
        return self._make_request(self.ENDPOINTS["proxy_add"], {"list": proxies[:100]})
    
    def update_proxies(
        self,
        proxies: List[Dict[str, Any]]
    ) -> GeeLarkResponse:
        """
        Update existing proxies in GeeLark.
        
        Args:
            proxies: List of proxy configs (max 100), each with:
                - id: Proxy ID (required)
                - scheme: "socks5", "http", or "https"
                - server: Proxy address
                - port: Proxy port
                - username: (optional)
                - password: (optional)
        """
        return self._make_request(self.ENDPOINTS["proxy_update"], {"list": proxies[:100]})
    
    def list_proxies(
        self,
        page: int = 1,
        page_size: int = 100,
        ids: Optional[List[str]] = None
    ) -> GeeLarkResponse:
        """
        Get all proxies from GeeLark.
        
        Args:
            page: Page number (min 1)
            page_size: Items per page (1-100)
            ids: Optional list of specific proxy IDs to filter
            
        Returns:
            Response with list of proxies containing id, serialNo, scheme, server, port, username, password
        """
        data = {
            "page": page,
            "pageSize": min(page_size, 100)
        }
        if ids:
            data["ids"] = ids
        return self._make_request(self.ENDPOINTS["proxy_list"], data)
    
    def delete_proxies(self, ids: List[str]) -> GeeLarkResponse:
        """
        Delete proxies from GeeLark.
        
        Args:
            ids: List of proxy IDs to delete (max 100)
            
        Note: Cannot delete proxies bound to an environment
        """
        return self._make_request(self.ENDPOINTS["proxy_delete"], {"ids": ids[:100]})
    
    # ===========================
    # App Management Methods
    # ===========================
    
    def list_installed_apps(
        self,
        phone_id: str,
        page: int = 1,
        page_size: int = 100
    ) -> GeeLarkResponse:
        """
        Get installed apps on a cloud phone.
        
        Args:
            phone_id: Cloud phone ID
            page: Page number (min 1)
            page_size: Items per page (1-100)
            
        Returns:
            Response with app info including installStatus:
            0-Installing, 1-Installed, 2-Failed, 3-Uninstalling, 
            4-Uninstalled, 5-Uninstall Failed
        """
        return self._make_request(self.ENDPOINTS["app_list"], {
            "envId": phone_id,
            "page": page,
            "pageSize": min(page_size, 100)
        })
    
    def install_app(
        self,
        phone_id: str,
        app_version_id: str
    ) -> GeeLarkResponse:
        """
        Install an app on a cloud phone.
        
        Args:
            phone_id: Cloud phone ID
            app_version_id: App version ID from app shop
        """
        return self._make_request(self.ENDPOINTS["app_install"], {
            "envId": phone_id,
            "appVersionId": app_version_id
        })
    
    def start_app(
        self,
        phone_id: str,
        app_version_id: Optional[str] = None,
        package_name: Optional[str] = None
    ) -> GeeLarkResponse:
        """
        Start an app on a cloud phone.
        
        Args:
            phone_id: Cloud phone ID
            app_version_id: App version ID (provide either this or package_name)
            package_name: App package name (e.g., com.zhiliaoapp.musically)
        """
        data = {"envId": phone_id}
        if app_version_id:
            data["appVersionId"] = app_version_id
        if package_name:
            data["packageName"] = package_name
        return self._make_request(self.ENDPOINTS["app_start"], data)
    
    def stop_app(
        self,
        phone_id: str,
        app_version_id: Optional[str] = None,
        package_name: Optional[str] = None
    ) -> GeeLarkResponse:
        """
        Stop an app on a cloud phone.
        
        Args:
            phone_id: Cloud phone ID
            app_version_id: App version ID (provide either this or package_name)
            package_name: App package name
        """
        data = {"envId": phone_id}
        if app_version_id:
            data["appVersionId"] = app_version_id
        if package_name:
            data["packageName"] = package_name
        return self._make_request(self.ENDPOINTS["app_stop"], data)
    
    def uninstall_app(
        self,
        phone_id: str,
        package_name: str
    ) -> GeeLarkResponse:
        """
        Uninstall an app from a cloud phone.
        
        Args:
            phone_id: Cloud phone ID
            package_name: App package name
        """
        return self._make_request(self.ENDPOINTS["app_uninstall"], {
            "envId": phone_id,
            "packageName": package_name
        })
    
    def search_app_shop(
        self,
        page: int = 1,
        page_size: int = 100,
        keyword: Optional[str] = None,
        get_upload_app: bool = False
    ) -> GeeLarkResponse:
        """
        Search apps in the GeeLark app shop.
        
        Args:
            page: Page number (min 1)
            page_size: Items per page (1-200)
            keyword: Search keyword (e.g., "tiktok")
            get_upload_app: Include uploaded apps
        """
        data = {
            "page": page,
            "pageSize": min(page_size, 200),
            "getUploadApp": get_upload_app
        }
        if keyword:
            data["key"] = keyword
        return self._make_request(self.ENDPOINTS["app_shop_list"], data)
    
    def add_team_app(
        self,
        app_id: str,
        version_id: str,
        install_group_ids: Optional[List[str]] = None
    ) -> GeeLarkResponse:
        """
        Add app to team applications (auto-installs on phone start).
        
        Args:
            app_id: Application ID
            version_id: Version ID
            install_group_ids: Environment group IDs (None = all, "0" = no group)
        """
        data = {"id": app_id, "versionId": version_id}
        if install_group_ids:
            data["installGroupIds"] = install_group_ids
        return self._make_request(self.ENDPOINTS["app_add"], data)
    
    def list_team_apps(
        self,
        page: int = 1,
        page_size: int = 100
    ) -> GeeLarkResponse:
        """Get team application list."""
        return self._make_request(self.ENDPOINTS["app_team_list"], {
            "page": page,
            "pageSize": min(page_size, 200)
        })
    
    def remove_team_app(self, team_app_id: str) -> GeeLarkResponse:
        """Remove app from team applications."""
        return self._make_request(self.ENDPOINTS["app_remove"], {"id": team_app_id})
    
    def batch_app_operation(
        self,
        action: int,
        group_ids: Optional[List[str]] = None,
        package_name: Optional[str] = None,
        version_id: Optional[str] = None
    ) -> GeeLarkResponse:
        """
        Batch operate apps on opened cloud phones.
        
        Args:
            action: 1=Start, 2=Close, 3=Restart, 4=Install, 5=Uninstall
            group_ids: Group IDs to target (None = all)
            package_name: App package name (for start/close/restart/uninstall)
            version_id: App version ID (required for install)
        """
        data = {"action": action}
        if group_ids:
            data["groupIds"] = group_ids
        if package_name:
            data["packageName"] = package_name
        if version_id:
            data["versionId"] = version_id
        return self._make_request(self.ENDPOINTS["app_operation_batch"], data)
    
    def install_tiktok(self, phone_id: str) -> GeeLarkResponse:
        """
        Helper to install TikTok on a phone.
        First searches for TikTok in app shop, then installs latest version.
        Specifically selects the main TikTok app, not TikTok Studio/Lite.
        """
        from loguru import logger
        
        # Search for TikTok
        search_result = self.search_app_shop(keyword="tiktok", page_size=20)
        if not search_result.success:
            return search_result
        
        items = search_result.data.get("items", [])
        logger.info(f"TikTok app search results: {[app.get('appName') for app in items]}")
        
        tiktok_app = None
        
        # Priority 1: Look for exact "TikTok" or package name
        for app in items:
            app_name = app.get("appName", "").strip()
            package_name = app.get("packageName", "")
            
            # The main TikTok app package is com.zhiliaoapp.musically or com.ss.android.ugc.trill
            if package_name in ["com.zhiliaoapp.musically", "com.ss.android.ugc.trill"]:
                tiktok_app = app
                logger.info(f"Found TikTok by package: {app_name} ({package_name})")
                break
            
            # Or exact name match (just "TikTok", not "TikTok Studio", "TikTok Lite", etc.)
            if app_name.lower() == "tiktok":
                tiktok_app = app
                logger.info(f"Found TikTok by exact name: {app_name}")
                break
        
        # Priority 2: Look for TikTok but NOT Studio/Lite
        if not tiktok_app:
            for app in items:
                app_name = app.get("appName", "").lower()
                if "tiktok" in app_name and "studio" not in app_name and "lite" not in app_name:
                    tiktok_app = app
                    logger.info(f"Found TikTok (excluding Studio/Lite): {app.get('appName')}")
                    break
        
        if not tiktok_app:
            return GeeLarkResponse(
                success=False, code=-1, message="TikTok not found in app shop",
                data=None, trace_id=""
            )
        
        # Get latest version
        versions = tiktok_app.get("appVersionList", [])
        if not versions:
            return GeeLarkResponse(
                success=False, code=-1, message="No TikTok versions available",
                data=None, trace_id=""
            )
        
        logger.info(f"Installing TikTok: {tiktok_app.get('appName')}, version ID: {versions[0].get('id')}")
        latest_version_id = versions[0].get("id")
        return self.install_app(phone_id, latest_version_id)

    
    # ===========================
    # Task Management Methods
    # ===========================
    
    def query_tasks(self, task_ids: List[str]) -> GeeLarkResponse:
        """
        Query task status and details.
        
        Args:
            task_ids: List of task IDs to query (max 100)
            
        Returns:
            Response with task details including:
            - id, planName, taskType, serialName, envId
            - scheduleAt (timestamp), status (1-7)
            - failCode, failDesc (if failed)
            - cost (execution time in seconds)
            - shareLink (if applicable)
        """
        return self._make_request(
            self.ENDPOINTS["task_query"],
            {"ids": task_ids[:100]}
        )
    
    def get_task_status_name(self, status_code: int) -> str:
        """Convert task status code to readable name."""
        return self.TASK_STATUS.get(status_code, "unknown")
    
    def add_task(
        self,
        phone_ids: List[str],
        task_type: int,
        variables: Optional[Dict[str, Any]] = None,
        schedule_at: Optional[int] = None
    ) -> GeeLarkResponse:
        """
        Create an automation task.
        
        Args:
            phone_ids: List of cloud phone IDs
            task_type: Task type constant (use TASK_TYPES)
            variables: Task-specific variables
            schedule_at: Scheduled time (timestamp in seconds)
        """
        # GeeLark API requires 'list' array format, not phoneIds
        task_list = []
        for phone_id in phone_ids:
            item = {"phoneId": phone_id}
            if variables:
                item["variables"] = variables
            task_list.append(item)
        
        data = {
            "taskType": task_type,
            "list": task_list
        }
        
        if schedule_at:
            data["scheduleAt"] = schedule_at
        
        logger.debug(f"Task add payload: {data}")
            
        return self._make_request(self.ENDPOINTS["task_add"], data)
    
    def run_custom_rpa(
        self,
        phone_id: str,
        flow_id: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> GeeLarkResponse:
        """
        Run a custom RPA Canvas flow.
        
        Args:
            phone_id: Cloud phone ID
            flow_id: Canvas flow ID from GeeLark marketplace/custom flows
            variables: Variables to pass to the flow
        """
        task_list = [{
            "phoneId": phone_id,
            "flowId": flow_id
        }]
        
        if variables:
            task_list[0]["variables"] = variables
        
        data = {
            "taskType": self.TASK_TYPES.get("CUSTOM", 42),
            "list": task_list
        }
        
        logger.debug(f"Custom RPA payload: {data}")
        
        return self._make_request(self.ENDPOINTS["task_add"], data)
    
    # ===========================
    # TikTok-Specific Task Helpers
    # ===========================
    
    def run_tiktok_warmup(
        self,
        phone_ids: List[str],
        duration_minutes: int = 45,
        max_likes: int = 30,
        max_follows: int = 10,
        max_comments: int = 5,
        schedule_at: Optional[int] = None
    ) -> GeeLarkResponse:
        """
        Run TikTok AI account warmup task.
        
        Args:
            phone_ids: List of phone IDs
            duration_minutes: Session duration
            max_likes: Maximum likes per session
            max_follows: Maximum follows per session
            max_comments: Maximum comments per session
            schedule_at: Scheduled time (timestamp)
        """
        variables = {
            "duration": duration_minutes,
            "maxLikes": max_likes,
            "maxFollows": max_follows,
            "maxComments": max_comments
        }
        
        return self.add_task(
            phone_ids=phone_ids,
            task_type=self.TASK_TYPES["TIKTOK_AI_WARMUP"],
            variables=variables,
            schedule_at=schedule_at
        )
    
    def run_tiktok_video_post(
        self,
        phone_ids: List[str],
        video_paths: List[str],
        captions: List[str],
        hashtags: Optional[List[str]] = None,
        schedule_at: Optional[int] = None
    ) -> GeeLarkResponse:
        """
        Run TikTok video posting task.
        
        Args:
            phone_ids: List of phone IDs
            video_paths: Paths to videos on phones
            captions: Video captions
            hashtags: Hashtags to include
            schedule_at: Scheduled time (timestamp)
        """
        variables = {
            "videoPaths": video_paths,
            "captions": captions
        }
        if hashtags:
            variables["hashtags"] = hashtags
            
        return self.add_task(
            phone_ids=phone_ids,
            task_type=self.TASK_TYPES["TIKTOK_VIDEO_POSTING"],
            variables=variables,
            schedule_at=schedule_at
        )
    
    def run_tiktok_login(
        self,
        phone_ids: List[str],
        credentials: List[Dict[str, str]],
        schedule_at: Optional[int] = None
    ) -> GeeLarkResponse:
        """
        Run TikTok account login task.
        
        Args:
            phone_ids: List of phone IDs
            credentials: List of {"email": "...", "password": "..."} dicts
            schedule_at: Scheduled time (timestamp)
        """
        return self.add_task(
            phone_ids=phone_ids,
            task_type=self.TASK_TYPES["TIKTOK_ACCOUNT_LOGIN"],
            variables={"credentials": credentials},
            schedule_at=schedule_at
        )
    
    # ===========================
    # Proxy Helper Methods
    # ===========================
    
    @staticmethod
    def format_proxy_string(
        host: str,
        port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        protocol: str = "socks5"
    ) -> str:
        """
        Format proxy credentials into GeeLark-compatible string.
        
        Returns: "protocol://user:pass@host:port" or "protocol://host:port"
        """
        if username and password:
            return f"{protocol}://{username}:{password}@{host}:{port}"
        return f"{protocol}://{host}:{port}"
    
    # ===========================
    # File Upload Methods
    # ===========================
    
    def get_upload_url(self, file_type: str) -> GeeLarkResponse:
        """
        Get temporary upload URL for a file (expires in 30 days).
        
        Args:
            file_type: File extension (e.g., "mp4", "jpg", "apk", "mp3")
            
        Returns:
            Response with uploadUrl (valid 30min) and resourceUrl
        """
        return self._make_request(self.ENDPOINTS["upload_get_url"], {"fileType": file_type})
    
    def upload_file_to_phone(
        self,
        phone_id: str,
        file_url: str
    ) -> GeeLarkResponse:
        """
        Upload a file to cloud phone's Downloads folder.
        Phone must be started before uploading.
        
        Args:
            phone_id: Cloud phone ID
            file_url: URL of the file to upload
            
        Returns:
            Response with taskId for status tracking
        """
        return self._make_request(self.ENDPOINTS["phone_upload_file"], {
            "id": phone_id,
            "fileUrl": file_url
        })
    
    def get_phone_upload_status(self, task_id: str) -> GeeLarkResponse:
        """
        Query upload status of file to cloud phone.
        Valid for 1 hour after initiating upload.
        
        Args:
            task_id: Task ID from upload_file_to_phone
            
        Returns:
            Response with status: 0=Failed, 1=Uploading, 2=Success, 3=Failed
        """
        return self._make_request(self.ENDPOINTS["phone_upload_file_result"], {"taskId": task_id})
    
    def upload_video_to_phone(
        self,
        phone_id: str,
        local_file_path: str
    ) -> GeeLarkResponse:
        """
        Upload a video file to cloud phone (convenience method).
        
        1. Gets temp upload URL
        2. Uploads file to GeeLark storage via PUT
        3. Transfers to phone
        
        Args:
            phone_id: Cloud phone ID
            local_file_path: Local path to video file
            
        Returns:
            Response with upload taskId or error
        """
        import os
        
        # Determine file type
        ext = os.path.splitext(local_file_path)[1].lstrip(".").lower()
        if ext not in ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "3gp"]:
            return GeeLarkResponse(
                success=False, code=-1, 
                message=f"Unsupported video format: {ext}",
                data=None, trace_id=""
            )
        
        # Get upload URL
        url_response = self.get_upload_url(ext)
        if not url_response.success:
            return url_response
        
        upload_url = url_response.data.get("uploadUrl")
        resource_url = url_response.data.get("resourceUrl")
        
        # Upload file via PUT request
        try:
            with open(local_file_path, "rb") as f:
                put_response = self.session.put(upload_url, data=f, timeout=120)
                if put_response.status_code != 200:
                    return GeeLarkResponse(
                        success=False, code=put_response.status_code,
                        message=f"File upload failed: {put_response.text}",
                        data=None, trace_id=""
                    )
        except Exception as e:
            return GeeLarkResponse(
                success=False, code=-1, message=str(e),
                data=None, trace_id=""
            )
        
        # Transfer to phone
        return self.upload_file_to_phone(phone_id, resource_url)
    
    # ===========================
    # ADB Management Methods
    # ===========================
    
    def set_adb_status(
        self,
        phone_ids: List[str],
        enable: bool
    ) -> GeeLarkResponse:
        """
        Enable or disable ADB on cloud phones.
        Supports Android 9, 11, 12, 13, 14, 15.
        Phone must be started first.
        
        Args:
            phone_ids: List of cloud phone IDs
            enable: True to enable, False to disable
            
        Note: Wait ~3 seconds after enabling before getting connection info.
        """
        return self._make_request(self.ENDPOINTS["adb_set_status"], {
            "ids": phone_ids,
            "open": enable
        })
    
    def get_adb_info(self, phone_ids: List[str]) -> GeeLarkResponse:
        """
        Get ADB connection information for cloud phones.
        
        Args:
            phone_ids: List of cloud phone IDs
            
        Returns:
            Response with items containing:
            - id: Phone ID
            - ip: Connection IP
            - port: Port number
            - pwd: Password
            - code: 0=success, 42002=not running, 49001=ADB not enabled
        """
        return self._make_request(self.ENDPOINTS["adb_get_data"], {"ids": phone_ids})
    
    # ===========================
    # Utility Methods
    # ===========================
    
    def test_connection(self) -> bool:
        """Test API connection and authentication."""
        response = self.list_phones(page=1, page_size=1)
        if response.success:
            logger.info("GeeLark API connection successful")
            return True
        else:
            logger.error(f"GeeLark API connection failed: {response.message}")
            return False
    
    def wait_for_task_completion(
        self,
        task_id: str,
        timeout_seconds: int = 300,
        poll_interval: int = 10
    ) -> GeeLarkResponse:
        """
        Wait for a task to complete with polling.
        
        Args:
            task_id: Task ID to monitor
            timeout_seconds: Max wait time
            poll_interval: Seconds between status checks
            
        Returns:
            Final task status response
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            response = self.query_tasks([task_id])
            
            if response.success and response.data:
                items = response.data.get("items", [])
                if items:
                    task = items[0]
                    status = task.get("status")
                    
                    # 3=completed, 4=failed, 7=cancelled
                    if status in [3, 4, 7]:
                        return response
            
            time.sleep(poll_interval)
        
        return GeeLarkResponse(
            success=False,
            code=-1,
            message="Task polling timeout",
            data=None,
            trace_id=""
        )
