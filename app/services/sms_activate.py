"""
SMS Verification Service
=========================
Provides virtual phone numbers for SMS verification during TikTok registration.

Supported Providers:
- HeroSMS (primary) - Successor to SMS-Activate
- SMSPool (backup)

API Documentation:
- HeroSMS: https://herosms.com/api
- SMSPool: https://smspool.net/api
"""

import os
import time
import requests
from typing import Optional, Dict, Any, Tuple
from loguru import logger
from dataclasses import dataclass


@dataclass
class SMSNumber:
    """Represents a rented virtual phone number."""
    activation_id: str
    phone_number: str
    country: str
    service: str
    provider: str = "herosms"
    status: str = "waiting"
    code: Optional[str] = None


class SMSClient:
    """
    Unified SMS verification client supporting HeroSMS (successor to SMS-Activate).
    
    Usage:
        client = SMSClient()
        number = client.get_number(service="tiktok", country="usa")
        code = client.wait_for_code(number.activation_id, timeout=120)
        client.complete_activation(number.activation_id)
    """
    
    # HeroSMS API - using main domain (api subdomain doesn't exist)
    # Fallback order: hero-sms.com, then get-sms.com (compatible API)
    BASE_URL = "https://hero-sms.com/stubs/handler_api.php"
    
    # Service codes - TikTok has multiple possible codes depending on provider
    # We'll try these in order until one works
    TIKTOK_SERVICE_CODES = ["tiktok", "douyin", "tt", "dy", "lf", "tk"]
    
    # Primary service codes for popular platforms
    SERVICES = {
        "tiktok": "tiktok",   # Try this first, fallback to others
        "instagram": "ig",
        "facebook": "fb",
        "google": "go",
        "telegram": "tg",
        "whatsapp": "wa",
    }

    
    # Country codes (from HeroSMS API - use getCountries to verify)
    # Note: USA is typically country 12, but may vary
    COUNTRIES = {
        "usa": 12,        # United States
        "uk": 16,         # United Kingdom
        "canada": 36,     # Canada
        "russia": 0,      # Russia (default)
        "kazakhstan": 2,  # Kazakhstan (cheap)
        "ukraine": 1,     # Ukraine
        "indonesia": 6,   # Indonesia (often available)
        "india": 22,      # India
        "philippines": 4, # Philippines
        "any": 0,         # Any available country
    }

    
    # Status codes for setStatus
    STATUS_CODES = {
        "cancel": 8,           # Cancel activation
        "sms_sent": 1,         # Notify SMS has been sent
        "code_received": 6,    # Activation completed successfully
        "request_another": 3,  # Request another SMS
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize HeroSMS client.
        
        Args:
            api_key: API key from herosms.com dashboard.
                    Falls back to HEROSMS_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("HEROSMS_API_KEY")
        if not self.api_key:
            logger.warning("HeroSMS API key not configured")
    
    def _make_request(self, params: Dict[str, Any]) -> str:
        """Make API request and return response text."""
        params["api_key"] = self.api_key
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            logger.debug(f"HeroSMS response: {response.text}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"HeroSMS API error: {e}")
            raise
    
    def get_balance(self) -> float:
        """Get current account balance in USD."""
        result = self._make_request({"action": "getBalance"})
        
        if result.startswith("ACCESS_BALANCE:"):
            balance = float(result.split(":")[1])
            logger.info(f"HeroSMS balance: ${balance:.2f}")
            return balance
        else:
            logger.error(f"Failed to get balance: {result}")
            return 0.0
    
    def get_number(
        self,
        service: str = "tiktok",
        country: str = "usa",
        max_price: Optional[float] = None
    ) -> Optional[SMSNumber]:
        """
        Request a virtual phone number for SMS verification.
        For TikTok, tries multiple service codes until one works.
        """
        country_code = self.COUNTRIES.get(country.lower(), country)
        
        # For TikTok, try multiple service codes (different providers use different codes)
        if service.lower() == "tiktok":
            service_codes_to_try = self.TIKTOK_SERVICE_CODES
        else:
            service_codes_to_try = [self.SERVICES.get(service.lower(), service)]
        
        for service_code in service_codes_to_try:
            params = {
                "action": "getNumber",
                "service": service_code,
                "country": country_code,
            }
            
            if max_price:
                params["maxPrice"] = max_price
            
            logger.info(f"Trying service code '{service_code}' for {country}...")
            
            try:
                result = self._make_request(params)
            except Exception as e:
                logger.warning(f"Request failed for code '{service_code}': {e}")
                continue
            
            # Response format: ACCESS_NUMBER:activation_id:phone_number
            if result.startswith("ACCESS_NUMBER:"):
                parts = result.split(":")
                activation_id = parts[1]
                phone_number = parts[2]
                
                # Format phone number (add + if not present)
                if not phone_number.startswith("+"):
                    phone_number = f"+{phone_number}"
                
                logger.info(f"SUCCESS with code '{service_code}': {phone_number} (ID: {activation_id})")
                
                return SMSNumber(
                    activation_id=activation_id,
                    phone_number=phone_number,
                    country=country,
                    service=service,
                    provider="herosms",
                    status="waiting"
                )
            
            # Check if it's a "no numbers" error - try next code
            if result in ["NO_NUMBERS", "NO_NUMBERS_AVAILABLE"]:
                logger.warning(f"No numbers for code '{service_code}', trying next...")
                continue
            
            # For other errors, log and try next
            logger.warning(f"Code '{service_code}' returned: {result}")
        
        # All codes failed
        logger.error(f"All service codes failed for {service} in {country}")
        return None

    
    def get_status(self, activation_id: str) -> Tuple[str, Optional[str]]:
        """
        Check status of an activation and get SMS code if received.
        
        Args:
            activation_id: The activation ID from get_number()
            
        Returns:
            Tuple of (status, code) where code is None if not yet received
        """
        result = self._make_request({
            "action": "getStatus",
            "id": activation_id
        })
        
        # Response formats:
        # STATUS_WAIT_CODE - waiting for SMS
        # STATUS_WAIT_RETRY - waiting for retry
        # STATUS_CANCEL - cancelled
        # STATUS_OK:code - code received
        
        if result.startswith("STATUS_OK:"):
            code = result.split(":")[1]
            logger.info(f"SMS code received: {code}")
            return ("received", code)
        elif result == "STATUS_WAIT_CODE":
            return ("waiting", None)
        elif result == "STATUS_WAIT_RETRY":
            return ("retry", None)
        elif result == "STATUS_CANCEL":
            return ("cancelled", None)
        else:
            logger.warning(f"Unknown status: {result}")
            return ("unknown", None)
    
    def wait_for_code(
        self,
        activation_id: str,
        timeout: int = 120,
        poll_interval: int = 5
    ) -> Optional[str]:
        """
        Wait for SMS verification code with polling.
        
        Args:
            activation_id: The activation ID from get_number()
            timeout: Maximum seconds to wait
            poll_interval: Seconds between status checks
            
        Returns:
            Verification code string, or None if timeout/cancelled
        """
        logger.info(f"Waiting for SMS code (timeout: {timeout}s)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status, code = self.get_status(activation_id)
            
            if status == "received" and code:
                return code
            elif status == "cancelled":
                logger.warning("Activation was cancelled")
                return None
            
            time.sleep(poll_interval)
        
        logger.warning(f"Timeout waiting for SMS code after {timeout}s")
        return None
    
    def set_status(self, activation_id: str, status: int) -> bool:
        """
        Set activation status (complete, cancel, request another SMS).
        
        Args:
            activation_id: The activation ID
            status: Status code:
                    1 = SMS sent (notify ready for code)
                    3 = Request another SMS
                    6 = Activation completed successfully
                    8 = Cancel activation
                    
        Returns:
            True if successful
        """
        result = self._make_request({
            "action": "setStatus",
            "id": activation_id,
            "status": status
        })
        
        success = result.startswith("ACCESS_")
        if success:
            logger.info(f"Set activation {activation_id} status to {status}")
        else:
            logger.error(f"Failed to set status: {result}")
        
        return success
    
    def complete_activation(self, activation_id: str) -> bool:
        """Mark activation as successfully completed."""
        return self.set_status(activation_id, self.STATUS_CODES["code_received"])
    
    def cancel_activation(self, activation_id: str) -> bool:
        """Cancel an activation (refund if no SMS received)."""
        return self.set_status(activation_id, self.STATUS_CODES["cancel"])
    
    def request_another_sms(self, activation_id: str) -> bool:
        """Request another SMS to be sent."""
        return self.set_status(activation_id, self.STATUS_CODES["request_another"])


class SMSPoolClient:
    """
    SMSPool.net client - better TikTok availability than most providers.
    
    API Docs: https://www.smspool.net/article/how-to-use-the-smspool-api
    """
    
    BASE_URL = "https://api.smspool.net"
    
    # Country names for SMSPool (uses country names, not codes)
    COUNTRIES = {
        "usa": "US",
        "uk": "GB",
        "canada": "CA",
        "russia": "RU",
        "indonesia": "ID",
        "philippines": "PH",
        "india": "IN",
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SMSPOOL_API_KEY")
        if not self.api_key:
            logger.warning("SMSPool API key not configured")
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict:
        """Make POST request to SMSPool API."""
        data["key"] = self.api_key
        
        try:
            response = requests.post(f"{self.BASE_URL}/{endpoint}", data=data, timeout=30)
            response.raise_for_status()
            logger.debug(f"SMSPool response: {response.text}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"SMSPool API error: {e}")
            raise
    
    def get_balance(self) -> float:
        """Get current account balance."""
        try:
            result = self._make_request("request/balance", {})
            balance = float(result.get("balance", 0))
            logger.info(f"SMSPool balance: ${balance:.2f}")
            return balance
        except Exception as e:
            logger.error(f"Failed to get SMSPool balance: {e}")
            return 0.0
    
    def get_number(self, service: str = "tiktok", country: str = "usa") -> Optional[SMSNumber]:
        """Request a virtual phone number."""
        country_code = self.COUNTRIES.get(country.lower(), "US")
        
        try:
            result = self._make_request("purchase/sms", {
                "service": "395",  # TikTok service ID
                "country": country_code,
            })
            
            if result.get("success") == 1:
                phone = result.get("phonenumber", "")
                order_id = str(result.get("order_id", ""))
                
                if not phone.startswith("+"):
                    phone = f"+{phone}"
                
                logger.info(f"SMSPool got number: {phone} (Order: {order_id})")
                
                return SMSNumber(
                    activation_id=order_id,
                    phone_number=phone,
                    country=country,
                    service=service,
                    provider="smspool",
                    status="waiting"
                )
            else:
                error = result.get("message", "Unknown error")
                logger.error(f"SMSPool get_number failed: {error}")
                return None
                
        except Exception as e:
            logger.error(f"SMSPool get_number error: {e}")
            return None
    
    def get_status(self, activation_id: str) -> Tuple[str, Optional[str]]:
        """Check SMS status."""
        try:
            result = self._make_request("sms/check", {"orderid": activation_id})
            
            status = result.get("status")
            if status == 3:  # SMS received
                code = result.get("sms", "")
                # Extract code from SMS text (usually 6 digits)
                import re
                code_match = re.search(r'\d{4,6}', str(code))
                if code_match:
                    code = code_match.group()
                logger.info(f"SMSPool code received: {code}")
                return ("received", code)
            elif status == 1:  # Pending
                return ("waiting", None)
            elif status == 4:  # Expired/Cancelled
                return ("cancelled", None)
            else:
                return ("waiting", None)
                
        except Exception as e:
            logger.error(f"SMSPool get_status error: {e}")
            return ("unknown", None)
    
    def wait_for_code(self, activation_id: str, timeout: int = 120, poll_interval: int = 5) -> Optional[str]:
        """Wait for SMS code with polling."""
        logger.info(f"SMSPool waiting for code (timeout: {timeout}s)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status, code = self.get_status(activation_id)
            
            if status == "received" and code:
                return code
            elif status == "cancelled":
                return None
            
            time.sleep(poll_interval)
        
        logger.warning(f"SMSPool timeout after {timeout}s")
        return None
    
    def cancel_activation(self, activation_id: str) -> bool:
        """Cancel an order."""
        try:
            result = self._make_request("sms/cancel", {"orderid": activation_id})
            return result.get("success") == 1
        except:
            return False
    
    def complete_activation(self, activation_id: str) -> bool:
        """Mark activation complete (no explicit API call needed for SMSPool)."""
        return True


# Alias for backward compatibility
SMSActivateClient = SMSClient


def get_sms_client() -> Optional[SMSClient]:
    """Get configured SMS client (HeroSMS primary)."""
    api_key = os.getenv("HEROSMS_API_KEY")
    if not api_key:
        logger.warning("HEROSMS_API_KEY not set - SMS verification disabled")
        return None
    return SMSClient(api_key=api_key)


def get_smspool_client() -> Optional[SMSPoolClient]:
    """Get configured SMSPool client (backup provider)."""
    api_key = os.getenv("SMSPOOL_API_KEY")
    if not api_key:
        logger.debug("SMSPOOL_API_KEY not set - backup SMS provider not available")
        return None
    return SMSPoolClient(api_key=api_key)


def get_any_sms_client():
    """Get any available SMS client (tries HeroSMS first, then SMSPool)."""
    client = get_sms_client()
    if client:
        return client
    return get_smspool_client()
