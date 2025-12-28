#!/usr/bin/env python3

# KMI Application with MFA Authentication
# This replaces the original main.py with MFA-protected access.

from kmi_client_mfa import KMIClientMFA
import sys
import getpass

def main():
    print("=" * 50)
    print("  KMI APPLICATION - MFA PROTECTED")
    print("=" * 50)
    print()
    
    # --- AUTHENTICATION ---
    user_id = input("User ID: ").strip()
    
    # Use getpass for token to hide input
    vault_token = getpass.getpass("Vault Token: ")
    
    totp_code = input("MFA Code (6 digits): ").strip()
    
    print()
    print("Authenticating...")
    
    # Initialize client with MFA
    kmi = KMIClientMFA(
        user_id=user_id,
        vault_token=vault_token,
        totp_code=totp_code
    )
    
    # Check authentication result
    if not kmi.is_connected:
        error_messages = {
            "MFA_NOT_ENROLLED": "User is not enrolled in MFA. Run enroll_mfa.py first.",
            "MFA_INVALID_CODE": "Invalid MFA code. Check your authenticator app.",
            "VAULT_AUTH_FAILED": "Vault authentication failed. Check your token."
        }
        msg = error_messages.get(kmi.auth_error, f"Unknown error: {kmi.auth_error}")
        sys.exit(f"✗ Authentication Failed: {msg}")
    
    print("✓ Authentication successful!")
    print("-" * 50)
    print()
    
    # Feature 1: Digital Signatures
    print("FEATURE: Digital Signature Storage")
    current_user = "student_01"
    signature_data = "a1b2-c3d4-e5f6-secure-hash"
    
    print(f"  Processing signature for user: {current_user}...")
    success, msg = kmi.store_digital_signature(current_user, signature_data)
    
    if success:
        print(f"  ✓ SUCCESS: {msg}")
    else:
        print(f"  ✗ ERROR: {msg}")
    print()
    
    # Feature 2: Credential Retrieval
    print("FEATURE: Database Credential Retrieval")
    print("  Requesting database access...")
    db_pass = kmi.retrieve_db_credentials()
    
    if db_pass:
        print(f"  ✓ Access Granted. DB Password: {db_pass}")
    else:
        print("  ✗ Access Denied: Could not retrieve credentials.")
    
    print()
    print("-" * 50)
    print("Session complete.")


if __name__ == "__main__":
    main()
