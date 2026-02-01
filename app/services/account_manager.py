"""
Account Manager Service
=======================
Handles account lifecycle: creation, warmup, and status management.
"""

import random
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from loguru import logger

from app.models.account import Account, Proxy, AccountStatus, ActivityLog
from app.services.geelark_client import GeeLarkClient
from app.config import get_settings

settings = get_settings()


class AccountManager:
    """
    Manages TikTok account lifecycle through GeeLark cloud phones.
    """
    
    def __init__(self, db: Session, geelark_client: GeeLarkClient):
        self.db = db
        self.geelark = geelark_client
    
    # ===========================
    # Proxy Management
    # ===========================
    
    def add_proxies_from_list(self, proxy_strings: List[str], protocol: str = "HTTP") -> List[Proxy]:
        """
        Add proxies from list of strings.
        
        Format: host:port:username:password or host:port
        """
        proxies = []
        for proxy_str in proxy_strings:
            parts = proxy_str.strip().split(":")
            if len(parts) >= 2:
                proxy = Proxy(
                    host=parts[0],
                    port=int(parts[1]),
                    username=parts[2] if len(parts) > 2 else None,
                    password=parts[3] if len(parts) > 3 else None,
                    protocol=protocol,
                    is_assigned=False,
                    is_active=True
                )
                self.db.add(proxy)
                proxies.append(proxy)
        
        self.db.commit()
        logger.info(f"Added {len(proxies)} proxies to pool")
        return proxies
    
    def get_available_proxy(self) -> Optional[Proxy]:
        """Get an unassigned, active proxy."""
        proxy = self.db.query(Proxy).filter(
            Proxy.is_assigned == False,
            Proxy.is_active == True
        ).first()
        return proxy
    
    def assign_proxy_to_account(self, account: Account, proxy: Proxy) -> bool:
        """Assign a proxy to an account."""
        proxy.is_assigned = True
        account.proxy_id = proxy.id
        self.db.commit()
        return True
    
    # ===========================
    # Account Creation
    # ===========================
    
    def create_single_account(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password: Optional[str] = None,
        proxy: Optional[Proxy] = None
    ) -> Optional[Account]:
        """
        Create a single TikTok account with GeeLark cloud phone.
        
        Steps:
        1. Get or assign proxy
        2. Create GeeLark cloud phone profile
        3. Install TikTok app
        4. Store in database
        """
        # Get proxy if not provided
        if not proxy:
            proxy = self.get_available_proxy()
            if not proxy:
                logger.error("No available proxies")
                return None
        
        # Create GeeLark profile
        proxy_config = proxy.to_geelark_format() if proxy else None
        
        response = self.geelark.create_phone(
            name=name,
            proxy_config=proxy_config,
            os_version="12",
            tags=["tiktok_automation"],
            randomize_fingerprint=True
        )
        
        if not response.success:
            logger.error(f"Failed to create phone: {response.message}")
            return None
        
        geelark_profile_id = response.data.get("phoneId") or response.data.get("id")
        
        # Create account in DB
        account = Account(
            geelark_profile_id=geelark_profile_id,
            geelark_profile_name=name,
            email=email,
            phone=phone,
            password=password,
            status=AccountStatus.CREATED,
            proxy_id=proxy.id if proxy else None
        )
        
        if proxy:
            proxy.is_assigned = True
        
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        
        # Log activity
        self._log_activity(account.id, "account_created", {
            "geelark_profile_id": geelark_profile_id,
            "proxy": f"{proxy.host}:{proxy.port}" if proxy else None
        })
        
        logger.info(f"Created account {account.id} with GeeLark profile {geelark_profile_id}")
        return account
    
    def batch_create_accounts(
        self,
        count: int,
        credentials: Optional[List[Dict[str, str]]] = None,
        name_prefix: str = "TikTok_Account"
    ) -> List[Account]:
        """
        Create multiple accounts in batch.
        
        Args:
            count: Number of accounts to create
            credentials: List of {"email": "...", "phone": "...", "password": "..."} dicts
            name_prefix: Prefix for profile names
        """
        accounts = []
        
        for i in range(count):
            creds = credentials[i] if credentials and i < len(credentials) else {}
            
            account = self.create_single_account(
                name=f"{name_prefix}_{i+1}_{datetime.now().strftime('%Y%m%d')}",
                email=creds.get("email"),
                phone=creds.get("phone"),
                password=creds.get("password")
            )
            
            if account:
                accounts.append(account)
            
            # Small delay between creations to avoid rate limits
            import time
            time.sleep(0.5)
        
        logger.info(f"Created {len(accounts)}/{count} accounts")
        return accounts
    
    # ===========================
    # Account Lifecycle
    # ===========================
    
    def start_account(self, account_id: int) -> bool:
        """Start the GeeLark cloud phone for an account."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or not account.geelark_profile_id:
            return False
        
        response = self.geelark.start_phone(account.geelark_profile_id)
        
        if response.success:
            self._log_activity(account_id, "phone_started", {"profile_id": account.geelark_profile_id})
            return True
        
        logger.error(f"Failed to start phone: {response.message}")
        return False
    
    def stop_account(self, account_id: int) -> bool:
        """Stop the GeeLark cloud phone for an account."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or not account.geelark_profile_id:
            return False
        
        response = self.geelark.stop_phone(account.geelark_profile_id)
        
        if response.success:
            self._log_activity(account_id, "phone_stopped", {"profile_id": account.geelark_profile_id})
            return True
        return False
    
    def pause_account(self, account_id: int) -> bool:
        """Pause automation for an account."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False
        
        self.stop_account(account_id)
        account.status = AccountStatus.PAUSED
        self.db.commit()
        
        self._log_activity(account_id, "account_paused", {})
        return True
    
    def resume_account(self, account_id: int) -> bool:
        """Resume automation for an account."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False
        
        account.status = AccountStatus.ACTIVE if account.warmup_complete else AccountStatus.WARMING_UP
        self.db.commit()
        
        self._log_activity(account_id, "account_resumed", {"new_status": account.status.value})
        return True
    
    def mark_banned(self, account_id: int, reason: str = "") -> bool:
        """Mark an account as banned."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False
        
        self.stop_account(account_id)
        account.status = AccountStatus.BANNED
        account.notes = f"Banned: {reason}" if reason else "Banned"
        self.db.commit()
        
        self._log_activity(account_id, "account_banned", {"reason": reason})
        logger.warning(f"Account {account_id} marked as banned: {reason}")
        return True
    
    # ===========================
    # TikTok App Management
    # ===========================
    
    def install_tiktok(self, account_id: int, use_marketplace: bool = True) -> bool:
        """
        Install TikTok on an account's cloud phone.
        
        Args:
            account_id: Account ID
            use_marketplace: Use GeeLark marketplace version (recommended for flows)
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or not account.geelark_profile_id:
            return False
        
        if use_marketplace:
            response = self.geelark.install_app(
                phone_id=account.geelark_profile_id,
                app_name="TikTok"
            )
        else:
            # Custom APK - could add APK URL support here
            response = self.geelark.install_app(
                phone_id=account.geelark_profile_id,
                app_name="TikTok"
            )
        
        if response.success:
            self._log_activity(account_id, "tiktok_installed", {
                "marketplace": use_marketplace
            })
            return True
        
        logger.error(f"Failed to install TikTok: {response.message}")
        return False
    
    # ===========================
    # Status & Metrics
    # ===========================
    
    def get_account(self, account_id: int) -> Optional[Account]:
        """Get account by ID."""
        return self.db.query(Account).filter(Account.id == account_id).first()
    
    def get_all_accounts(
        self,
        status: Optional[AccountStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Account]:
        """Get all accounts with optional filtering."""
        query = self.db.query(Account)
        if status:
            query = query.filter(Account.status == status)
        return query.offset(offset).limit(limit).all()
    
    def get_accounts_ready_for_warmup(self) -> List[Account]:
        """Get accounts that need warmup today."""
        return self.db.query(Account).filter(
            Account.status == AccountStatus.WARMING_UP,
            Account.warmup_complete == False
        ).all()
    
    def get_accounts_ready_for_posting(self) -> List[Account]:
        """Get accounts ready to post content."""
        return self.db.query(Account).filter(
            Account.status.in_([AccountStatus.ACTIVE, AccountStatus.POSTING]),
            Account.warmup_complete == True
        ).all()
    
    def sync_metrics_from_geelark(self, account_id: int) -> bool:
        """Sync account metrics from GeeLark (if available)."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or not account.geelark_profile_id:
            return False
        
        response = self.geelark.get_phone_detail(account.geelark_profile_id)
        if response.success and response.data:
            # Update any available metrics
            account.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    # ===========================
    # Activity Logging
    # ===========================
    
    def _log_activity(
        self,
        account_id: int,
        action_type: str,
        details: Dict[str, Any],
        success: bool = True,
        error: Optional[str] = None
    ):
        """Log an activity for an account."""
        log = ActivityLog(
            account_id=account_id,
            action_type=action_type,
            action_details=details,
            success=success,
            error_message=error
        )
        self.db.add(log)
        self.db.commit()
    
    def get_activity_logs(
        self,
        account_id: Optional[int] = None,
        action_type: Optional[str] = None,
        limit: int = 50
    ) -> List[ActivityLog]:
        """Get activity logs with optional filtering."""
        query = self.db.query(ActivityLog)
        if account_id:
            query = query.filter(ActivityLog.account_id == account_id)
        if action_type:
            query = query.filter(ActivityLog.action_type == action_type)
        return query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    
    # ===========================
    # Full Automation Setup
    # ===========================
    
    def full_automation_setup(
        self,
        proxy_string: str,
        name_prefix: str = "",
        max_username_retries: int = 5,
        callback: callable = None
    ) -> Dict[str, Any]:
        """
        Complete zero-touch automation: Proxy → Phone → TikTok → Account → Warmup.
        
        Args:
            proxy_string: Proxy in format "protocol://user:pass@host:port" 
                         or "host:port:user:pass"
            name_prefix: Optional prefix for the account name
            max_username_retries: Max attempts if username is taken
            callback: Optional function to call with status updates
            
        Returns:
            Dict with status, account_id, credentials, and any errors
        """
        from app.services.credential_generator import generate_credentials
        from app.services.credential_vault import get_vault
        import time
        
        result = {
            "success": False,
            "steps_completed": [],
            "account_id": None,
            "phone_id": None,
            "credentials": None,
            "error": None
        }
        
        def update_status(step: str, status: str = "running"):
            result["steps_completed"].append({"step": step, "status": status})
            if callback:
                callback(step, status)
            logger.info(f"Automation step [{status}]: {step}")
        
        try:
            # Step 1: Parse and create proxy
            update_status("Parsing proxy configuration")
            proxy = self._parse_and_create_proxy(proxy_string)
            if not proxy:
                raise Exception("Failed to parse proxy string")
            update_status("Proxy created", "complete")
            
            # Step 2: Create cloud phone with Android 15
            update_status("Creating Android 15 cloud phone")
            phone_name = f"TikTok_{name_prefix}_{datetime.now().strftime('%m%d_%H%M')}"
            
            response = self.geelark.create_single_phone(
                name=phone_name,
                proxy_string=proxy_string,
                mobile_type="Android 15",  # Latest Android
                region="USA-US",
                language="default"
            )
            
            if not response.success:
                # Fallback to Android 12 if 15 not available
                response = self.geelark.create_single_phone(
                    name=phone_name,
                    proxy_string=proxy_string,
                    mobile_type="Android 12",
                    region="USA-US",
                    language="default"
                )
            
            if not response.success:
                raise Exception(f"Failed to create phone: {response.message}")
            
            # Debug: Log the response to understand structure
            logger.info(f"Phone creation response data: {response.data}")
            
            # Extract phone ID from response - handle different response formats
            phone_id = None
            if isinstance(response.data, dict):
                phone_id = response.data.get("phoneId") or response.data.get("id")
                # Check if it's in a nested list (batch create returns list)
                if not phone_id and "data" in response.data:
                    data_list = response.data.get("data", [])
                    if data_list and isinstance(data_list, list):
                        phone_id = data_list[0].get("phoneId") or data_list[0].get("id")
            elif isinstance(response.data, list) and response.data:
                phone_id = response.data[0].get("phoneId") or response.data[0].get("id")
            
            if not phone_id:
                raise Exception(f"Could not extract phone ID from response: {response.data}")
            
            logger.info(f"Extracted phone_id: {phone_id}")
            result["phone_id"] = phone_id
            update_status("Phone created", "complete")
            
            # Step 3: Start the phone
            update_status("Starting cloud phone")
            start_response = self.geelark.start_phones([phone_id])
            logger.info(f"Start phone response: success={start_response.success}, message={start_response.message}")
            if not start_response.success:
                raise Exception(f"Failed to start phone: {start_response.message}")
            
            # Wait for phone to boot
            time.sleep(15)
            update_status("Phone started", "complete")

            
            # Step 4: Install TikTok
            update_status("Installing TikTok")
            install_response = self.geelark.install_tiktok(phone_id)
            if not install_response.success:
                raise Exception(f"Failed to install TikTok: {install_response.message}")
            
            # Wait for installation
            time.sleep(10)
            update_status("TikTok installed", "complete")
            
            # Step 5: Generate credentials and create TikTok account
            update_status("Creating TikTok account")
            
            account_created = False
            credentials = None
            
            for attempt in range(max_username_retries):
                username, email, password = generate_credentials(name_prefix)
                
                # Use GeeLark's login/registration RPA
                login_response = self.geelark.run_tiktok_login(
                    phone_id=phone_id,
                    login_type=1,  # Email registration
                    email=email,
                    password=password
                )
                
                if login_response.success:
                    credentials = {
                        "username": username,
                        "email": email,
                        "password": password
                    }
                    account_created = True
                    break
                elif "already taken" in str(login_response.message).lower():
                    logger.warning(f"Username {username} taken, retrying... ({attempt + 1}/{max_username_retries})")
                    continue
                else:
                    # Other error - might need to wait or handle differently
                    time.sleep(5)
            
            if not account_created:
                raise Exception(f"Failed to create TikTok account after {max_username_retries} attempts")
            
            result["credentials"] = credentials
            update_status("TikTok account created", "complete")
            
            # Step 6: Create account in our database
            update_status("Saving to database")
            account = Account(
                geelark_profile_id=phone_id,
                geelark_profile_name=phone_name,
                tiktok_username=credentials["username"],
                email=credentials["email"],
                password=credentials["password"],
                status=AccountStatus.WARMING_UP,
                proxy_id=proxy.id,
                warmup_day=1
            )
            
            proxy.is_assigned = True
            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)
            
            result["account_id"] = account.id
            update_status("Database record created", "complete")
            
            # Step 7: Store credentials in vault
            update_status("Securing credentials")
            vault = get_vault()
            vault.store_credential(
                account_id=account.id,
                username=credentials["username"],
                email=credentials["email"],
                password=credentials["password"],
                phone_id=phone_id,
                extra={"proxy": proxy_string}
            )
            update_status("Credentials secured", "complete")
            
            # Step 8: Start warmup
            update_status("Starting warmup process")
            warmup_response = self.geelark.run_tiktok_warmup(
                phone_id=phone_id,
                duration_minutes=20
            )
            
            if warmup_response.success:
                self._log_activity(account.id, "warmup_started", {
                    "day": 1,
                    "duration": 20
                })
            update_status("Warmup initiated", "complete")
            
            # Log the full automation
            self._log_activity(account.id, "full_automation_complete", {
                "phone_id": phone_id,
                "username": credentials["username"],
                "steps": len(result["steps_completed"])
            })
            
            result["success"] = True
            update_status("Automation complete!", "success")
            
        except Exception as e:
            result["error"] = str(e)
            result["steps_completed"].append({"step": "Error", "status": str(e)})
            logger.error(f"Full automation failed: {e}")
        
        return result
    
    def _parse_and_create_proxy(self, proxy_string: str) -> Optional[Proxy]:
        """Parse proxy string and create in database."""
        try:
            # Handle different formats
            # Format 1: protocol://user:pass@host:port
            # Format 2: host:port:user:pass
            # Format 3: host:port
            
            protocol = "HTTP"
            host = port = username = password = None
            
            if "://" in proxy_string:
                # URL format - check for different sub-formats
                parts = proxy_string.split("://")
                protocol = parts[0].upper()
                rest = parts[1]
                
                if "@" in rest:
                    # Standard URL format: user:pass@host:port
                    auth, host_port = rest.rsplit("@", 1)
                    if ":" in auth:
                        username, password = auth.split(":", 1)
                    host, port = host_port.rsplit(":", 1)
                else:
                    # Could be either host:port or host:port:user:pass
                    colon_parts = rest.split(":")
                    if len(colon_parts) >= 4:
                        # Format: protocol://host:port:user:pass
                        host = colon_parts[0]
                        port = colon_parts[1]
                        username = colon_parts[2]
                        password = ":".join(colon_parts[3:])  # In case password has colons
                    elif len(colon_parts) >= 2:
                        # Format: protocol://host:port
                        host, port = colon_parts[0], colon_parts[1]
                    else:
                        return None

            else:
                # Colon-separated format
                parts = proxy_string.split(":")
                if len(parts) >= 2:
                    host = parts[0]
                    port = parts[1]
                if len(parts) >= 4:
                    username = parts[2]
                    password = parts[3]
            
            if not host or not port:
                return None
            
            proxy = Proxy(
                host=host,
                port=int(port),
                username=username,
                password=password,
                protocol=protocol,
                is_assigned=False,
                is_active=True
            )
            self.db.add(proxy)
            self.db.commit()
            self.db.refresh(proxy)
            
            return proxy
            
        except Exception as e:
            logger.error(f"Failed to parse proxy: {e}")
            return None
    
    # ===========================
    # Ban Detection & Recovery
    # ===========================
    
    def check_account_health(self, account_id: int) -> Dict[str, Any]:
        """
        Check if an account is banned or has issues.
        
        Returns:
            Dict with health status and any detected issues
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or not account.geelark_profile_id:
            return {"healthy": False, "error": "Account not found"}
        
        # Check phone status
        status_response = self.geelark.get_phone_status([account.geelark_profile_id])
        
        result = {
            "healthy": True,
            "account_id": account_id,
            "phone_status": None,
            "issues": []
        }
        
        if status_response.success and status_response.data:
            phone_data = status_response.data[0] if status_response.data else {}
            result["phone_status"] = phone_data.get("status")
        
        # Check recent activity logs for ban indicators
        recent_logs = self.get_activity_logs(account_id=account_id, limit=10)
        
        ban_keywords = ["banned", "community guidelines", "violation", "suspended", "restricted"]
        
        for log in recent_logs:
            if log.error_message:
                for keyword in ban_keywords:
                    if keyword in log.error_message.lower():
                        result["healthy"] = False
                        result["issues"].append({
                            "type": "ban_detected",
                            "message": log.error_message,
                            "detected_at": log.created_at.isoformat()
                        })
                        break
        
        return result
    
    def handle_banned_account(
        self, 
        account_id: int,
        auto_recover: bool = True
    ) -> Dict[str, Any]:
        """
        Handle a banned account with recovery options.
        
        Strategy:
        1. First ban: Try creating new TikTok account on same phone
        2. Second ban: Delete phone, create new phone with same proxy
        
        Args:
            account_id: The banned account ID
            auto_recover: Whether to attempt automatic recovery
            
        Returns:
            Recovery result with new account info if successful
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return {"success": False, "error": "Account not found"}
        
        # Get proxy info before we potentially delete things
        proxy = self.db.query(Proxy).filter(Proxy.id == account.proxy_id).first()
        proxy_string = f"{proxy.protocol.lower()}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}" if proxy else None
        
        # Check how many times this proxy has had bans
        ban_count = self._get_proxy_ban_count(proxy.id) if proxy else 0
        
        result = {
            "success": False,
            "original_account_id": account_id,
            "ban_count": ban_count,
            "action_taken": None,
            "new_account_id": None,
            "new_phone_id": None
        }
        
        # Mark current account as banned
        self.mark_banned(account_id, "Community guidelines violation - auto-detected")
        
        if not auto_recover or not proxy_string:
            result["action_taken"] = "marked_banned_only"
            return result
        
        if ban_count < 2:
            # First ban on this proxy - try new account on same phone
            result["action_taken"] = "retry_account_creation"
            
            logger.info(f"First ban for proxy {proxy.id}, attempting new account on same phone")
            
            from app.services.credential_generator import generate_credentials
            from app.services.credential_vault import get_vault
            import time
            
            # Generate new credentials
            for attempt in range(5):
                username, email, password = generate_credentials()
                
                login_response = self.geelark.run_tiktok_login(
                    phone_id=account.geelark_profile_id,
                    login_type=1,
                    email=email,
                    password=password
                )
                
                if login_response.success:
                    # Create new account record
                    new_account = Account(
                        geelark_profile_id=account.geelark_profile_id,
                        geelark_profile_name=account.geelark_profile_name,
                        tiktok_username=username,
                        email=email,
                        password=password,
                        status=AccountStatus.WARMING_UP,
                        proxy_id=proxy.id,
                        warmup_day=1,
                        notes=f"Recovery account for banned #{account_id}"
                    )
                    
                    self.db.add(new_account)
                    self.db.commit()
                    self.db.refresh(new_account)
                    
                    # Store credentials
                    vault = get_vault()
                    vault.store_credential(
                        account_id=new_account.id,
                        username=username,
                        email=email,
                        password=password,
                        phone_id=account.geelark_profile_id,
                        extra={"recovered_from": account_id}
                    )
                    
                    # Start warmup
                    self.geelark.run_tiktok_warmup(
                        phone_id=account.geelark_profile_id,
                        duration_minutes=20
                    )
                    
                    self._log_activity(new_account.id, "account_recovered", {
                        "original_account": account_id,
                        "attempt": attempt + 1
                    })
                    
                    result["success"] = True
                    result["new_account_id"] = new_account.id
                    logger.info(f"Recovery successful - new account {new_account.id}")
                    return result
                
                time.sleep(3)
            
            # If we get here, account creation failed - treat as second ban
            logger.warning(f"Account creation failed on phone, escalating to phone recreation")
        
        # Second ban or account creation failed - recreate phone
        result["action_taken"] = "recreate_phone"
        
        logger.info(f"Second ban for proxy {proxy.id}, recreating phone")
        
        # Delete old phone
        self.geelark.stop_phones([account.geelark_profile_id])
        self.geelark.delete_phones([account.geelark_profile_id])
        
        # Create new phone with same proxy
        recovery_result = self.full_automation_setup(
            proxy_string=proxy_string,
            name_prefix=f"Recovery_{account_id}"
        )
        
        if recovery_result["success"]:
            result["success"] = True
            result["new_account_id"] = recovery_result["account_id"]
            result["new_phone_id"] = recovery_result["phone_id"]
            
            self._log_activity(recovery_result["account_id"], "phone_recreated", {
                "original_account": account_id,
                "original_phone": account.geelark_profile_id
            })
        else:
            result["error"] = recovery_result.get("error")
        
        return result
    
    def _get_proxy_ban_count(self, proxy_id: int) -> int:
        """Count how many accounts on this proxy have been banned."""
        return self.db.query(Account).filter(
            Account.proxy_id == proxy_id,
            Account.status == AccountStatus.BANNED
        ).count()
    
    def run_health_check_all(self) -> List[Dict[str, Any]]:
        """
        Run health check on all active accounts.
        
        Called by scheduler to detect bans early.
        """
        accounts = self.db.query(Account).filter(
            Account.status.in_([
                AccountStatus.WARMING_UP, 
                AccountStatus.ACTIVE, 
                AccountStatus.POSTING
            ])
        ).all()
        
        results = []
        
        for account in accounts:
            health = self.check_account_health(account.id)
            
            if not health["healthy"]:
                logger.warning(f"Unhealthy account detected: {account.id}")
                
                # Attempt auto-recovery
                recovery = self.handle_banned_account(account.id, auto_recover=True)
                health["recovery_result"] = recovery
            
            results.append(health)
        
        return results
