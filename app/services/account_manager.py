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
