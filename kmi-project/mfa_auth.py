#!/usr/bin/env python3

# MFA Authentication Module for KMI
# Uses TOTP (Time-based One-Time Password) for second factor authentication.

import pyotp
import qrcode
import json
import hashlib
import os
from pathlib import Path
from datetime import datetime

# Manages TOTP-based MFA for KMI users.
class MFAManager:
    def __init__(self, secrets_file: str = "mfa_secrets.json"):
        self.secrets_file = Path(secrets_file)
        self.secrets = self._load_secrets()
    
    def _load_secrets(self) -> dict:
        # Load MFA secrets from encrypted storage.
        if self.secrets_file.exists():
            with open(self.secrets_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_secrets(self):
        # Save MFA secrets to storage.
        # In production, encrypt this file with a master key from Vault
        with open(self.secrets_file, 'w') as f:
            json.dump(self.secrets, f, indent=2)
        # Restrict file permissions (Unix only)
        try:
            os.chmod(self.secrets_file, 0o600)
        except:
            pass
    
    def enroll_user(self, user_id: str, issuer: str = "KMI-Vault") -> tuple[str, str]:
        
        # Enroll a user in MFA. Returns (secret, provisioning_uri).
        # The provisioning URI can be encoded as QR for authenticator apps.
        
        secret = pyotp.random_base32()
        
        # Create provisioning URI for authenticator apps
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user_id,
            issuer_name=issuer
        )
        
        # Store the secret (hashed user_id as key for some obfuscation)
        user_key = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        self.secrets[user_key] = {
            "secret": secret,
            "user_id": user_id,
            "enrolled_at": datetime.now().strftime("%d-%b-%Y"),
            "enabled": True
        }
        self._save_secrets()
        
        return secret, provisioning_uri
    
    def generate_qr_code(self, provisioning_uri: str, output_path: str = "mfa_qr.png"):
        # Generate QR code for authenticator app enrollment.
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        return output_path
    
    def verify_totp(self, user_id: str, token: str) -> bool:
        # Verify a TOTP token for a user.
        user_key = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        
        if user_key not in self.secrets:
            return False
        
        user_data = self.secrets[user_key]
        if not user_data.get("enabled", False):
            return False
        
        totp = pyotp.TOTP(user_data["secret"])
        # valid_window=1 allows for slight time drift (30 sec before/after)
        return totp.verify(token, valid_window=1)
    
    def is_enrolled(self, user_id: str) -> bool:
        # Check if user has MFA enrolled.
        user_key = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        return user_key in self.secrets
    
    def get_current_totp(self, user_id: str) -> str | None:
        # Get current TOTP for a user (for testing/admin purposes only).
        user_key = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        if user_key not in self.secrets:
            return None
        totp = pyotp.TOTP(self.secrets[user_key]["secret"])
        return totp.now()
    
    def disable_mfa(self, user_id: str) -> bool:
        # Disable MFA for a user.
        user_key = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        if user_key in self.secrets:
            self.secrets[user_key]["enabled"] = False
            self._save_secrets()
            return True
        return False
    
    def remove_user(self, user_id: str) -> bool:
        # Completely remove MFA enrollment for a user.
        user_key = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        if user_key in self.secrets:
            del self.secrets[user_key]
            self._save_secrets()
            return True
        return False
