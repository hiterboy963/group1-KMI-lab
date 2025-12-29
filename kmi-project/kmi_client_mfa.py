#!/usr/bin/env python3

# KMI Client with MFA Support
# Wraps the original KMI client with mandatory TOTP verification.

import hvac
from mfa_auth import MFAManager

# KMI Client that requires MFA authentication.
class KMIClientMFA:
    
    def __init__(self, user_id: str, vault_token: str, totp_code: str,
                 vault_url: str = 'http://127.0.0.1:8200',
                 mfa_secrets_file: str = "mfa_secrets.json"):
        
        # Initialize KMI connection with MFA verification.
        # Args:
        #     user_id: User identifier for MFA lookup
        #     vault_token: HashiCorp Vault token
        #     totp_code: 6-digit TOTP code from authenticator app
        #     vault_url: Vault server URL
        #     mfa_secrets_file: Path to MFA secrets storage
        
        self.user_id = user_id
        self.mfa = MFAManager(mfa_secrets_file)
        self.client = None
        self.is_connected = False
        self.auth_error = None
        
        if not self.mfa.is_enrolled(user_id):
            self.auth_error = "MFA_NOT_ENROLLED"
            return
        
        if not self.mfa.verify_totp(user_id, totp_code):
            self.auth_error = "MFA_INVALID_CODE"
            return
        
        self.client = hvac.Client(url=vault_url, token=vault_token)
        
        if not self.client.is_authenticated():
            self.auth_error = "VAULT_AUTH_FAILED"
            return
        
        self.is_connected = True
    
    def store_digital_signature(self, user_id: str, signature_hash: str) -> tuple[bool, str]:
        # Securely stores a digital signature hash for a specific user.
        if not self.is_connected:
            return False, f"Not Connected: {self.auth_error}"

        try:
            secret_path = f"project/signatures/{user_id}"
            self.client.secrets.kv.v2.create_or_update_secret(
                path=secret_path,
                secret=dict(hash=signature_hash)
            )
            return True, "Signature Stored"
        except Exception as e:
            return False, str(e)

    def get_digital_signature(self, user_id: str) -> tuple[str | None, str]:
        # Retrieves a specific user's signature hash.
        if not self.is_connected:
            return None, "Not Connected"

        try:
            # We look for the exact path for THIS user
            secret_path = f"project/signatures/{user_id}"
            response = self.client.secrets.kv.v2.read_secret_version(path=secret_path)
            
            # Extract the hash from the dictionary
            return response['data']['data']['hash'], "Found"
        except hvac.exceptions.InvalidPath:
            return None, "Signature not found for this user."
        except Exception as e:
            return None, str(e)

    def store_db_credentials(self, username: str, db_data: dict) -> tuple[bool, str]:
        # Securely stores database credentials for a specific db user.
        if not self.is_connected:
            return False, "Not Connected"
        try:
            # Store at project/database/{username}
            self.client.secrets.kv.v2.create_or_update_secret(
                path=f'project/database/{username}',
                secret=db_data
            )
            return True, "Database Credentials Stored"
        except Exception as e:
            return False, str(e)

    def retrieve_db_credentials(self, target_username: str) -> dict | None:
        # Retrieves the database credentials for a specific db user.
        if not self.is_connected:
            return None
            
        try:
            # Fetch from project/database/{username}
            path = f'project/database/{target_username}'
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response['data']['data']
        except Exception:
            return None


def authenticate_with_mfa(user_id: str, vault_token: str, totp_code: str,
                          vault_url: str = 'http://127.0.0.1:8200') -> KMIClientMFA:
    
    # Convenience function to authenticate with MFA.
    # Returns an authenticated KMIClientMFA instance.
    
    return KMIClientMFA(
        user_id=user_id,
        vault_token=vault_token,
        totp_code=totp_code,
        vault_url=vault_url
    )