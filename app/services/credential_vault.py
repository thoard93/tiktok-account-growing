"""
Credential Vault
================
Secure storage for TikTok account credentials with Fernet encryption.
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path
from cryptography.fernet import Fernet
from loguru import logger


class CredentialVault:
    """
    Encrypted credential storage.
    
    Uses Fernet symmetric encryption to protect credentials at rest.
    The encryption key is stored separately from the data.
    """
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.key_file = self.data_dir / ".vault_key"
        self.vault_file = self.data_dir / "credentials.enc"
        
        self._fernet = self._init_encryption()
    
    def _init_encryption(self) -> Fernet:
        """Initialize or load encryption key."""
        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            # Restrict permissions on key file (Unix-like systems)
            try:
                os.chmod(self.key_file, 0o600)
            except Exception:
                pass  # Windows doesn't support chmod the same way
            
            logger.info(f"Generated new encryption key at {self.key_file}")
        
        return Fernet(key)
    
    def _load_vault(self) -> Dict[str, Any]:
        """Load and decrypt the vault."""
        if not self.vault_file.exists():
            return {"credentials": [], "created_at": datetime.utcnow().isoformat()}
        
        try:
            encrypted = self.vault_file.read_bytes()
            decrypted = self._fernet.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception as e:
            logger.error(f"Failed to decrypt vault: {e}")
            return {"credentials": [], "error": str(e)}
    
    def _save_vault(self, data: Dict[str, Any]):
        """Encrypt and save the vault."""
        try:
            json_bytes = json.dumps(data, indent=2).encode()
            encrypted = self._fernet.encrypt(json_bytes)
            self.vault_file.write_bytes(encrypted)
            logger.debug(f"Saved vault with {len(data.get('credentials', []))} credentials")
        except Exception as e:
            logger.error(f"Failed to save vault: {e}")
            raise
    
    def store_credential(
        self,
        account_id: int,
        username: str,
        email: str,
        password: str,
        phone_id: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a credential securely.
        
        Args:
            account_id: Internal account ID
            username: TikTok username
            email: Account email
            password: Account password
            phone_id: GeeLark phone ID
            extra: Any additional metadata
            
        Returns:
            True if stored successfully
        """
        vault = self._load_vault()
        
        credential = {
            "account_id": account_id,
            "username": username,
            "email": email,
            "password": password,
            "phone_id": phone_id,
            "created_at": datetime.utcnow().isoformat(),
            "extra": extra or {}
        }
        
        vault["credentials"].append(credential)
        vault["updated_at"] = datetime.utcnow().isoformat()
        
        self._save_vault(vault)
        logger.info(f"Stored credentials for account {account_id}: {username}")
        return True
    
    def get_credential(self, account_id: int) -> Optional[Dict[str, Any]]:
        """Get credentials for a specific account."""
        vault = self._load_vault()
        
        for cred in vault["credentials"]:
            if cred["account_id"] == account_id:
                return cred
        
        return None
    
    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """Get all stored credentials."""
        vault = self._load_vault()
        return vault.get("credentials", [])
    
    def update_credential(
        self,
        account_id: int,
        updates: Dict[str, Any]
    ) -> bool:
        """Update an existing credential."""
        vault = self._load_vault()
        
        for i, cred in enumerate(vault["credentials"]):
            if cred["account_id"] == account_id:
                vault["credentials"][i].update(updates)
                vault["credentials"][i]["updated_at"] = datetime.utcnow().isoformat()
                self._save_vault(vault)
                return True
        
        return False
    
    def delete_credential(self, account_id: int) -> bool:
        """Delete a credential."""
        vault = self._load_vault()
        
        original_len = len(vault["credentials"])
        vault["credentials"] = [
            c for c in vault["credentials"] 
            if c["account_id"] != account_id
        ]
        
        if len(vault["credentials"]) < original_len:
            self._save_vault(vault)
            return True
        
        return False
    
    def export_credentials_csv(self, output_path: str) -> str:
        """
        Export credentials to CSV (for backup).
        
        WARNING: This creates an unencrypted file!
        """
        import csv
        
        credentials = self.get_all_credentials()
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "account_id", "username", "email", "password", 
                "phone_id", "created_at"
            ])
            writer.writeheader()
            for cred in credentials:
                writer.writerow({
                    "account_id": cred["account_id"],
                    "username": cred["username"],
                    "email": cred["email"],
                    "password": cred["password"],
                    "phone_id": cred.get("phone_id", ""),
                    "created_at": cred.get("created_at", "")
                })
        
        logger.warning(f"Exported {len(credentials)} credentials to {output_path} (UNENCRYPTED)")
        return output_path


# Global vault instance
_vault: Optional[CredentialVault] = None


def get_vault(data_dir: str = "./data") -> CredentialVault:
    """Get or create the global vault instance."""
    global _vault
    if _vault is None:
        _vault = CredentialVault(data_dir)
    return _vault
