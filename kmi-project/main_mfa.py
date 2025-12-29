#!/usr/bin/env python3
from kmi_client_mfa import KMIClientMFA
import sys
import getpass
import time
import json

SECRETS_FILE = 'secrets.json'

def clear_screen():
    print("\n" * 2)

def load_local_secrets():
    """Helper to read the JSON file."""
    try:
        with open(SECRETS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    print("=" * 50)
    print("  🔐 KMI SECURE VAULT (MFA ENABLED)")
    print("=" * 50)
    
    # --- 1. AUTHENTICATION ---
    user_id = input("Enter User ID: ").strip()
    vault_token = getpass.getpass("Enter Vault Token: ")
    totp_code = input("Enter 6-digit MFA Code: ").strip()
    
    print("\nAuthenticating...")
    kmi = KMIClientMFA(user_id, vault_token, totp_code)
    
    if not kmi.is_connected:
        sys.exit(f"❌ ACCESS DENIED: {kmi.auth_error}")
    
    print("✓ IDENTITY CONFIRMED.")
    time.sleep(1)

    # --- 2. MENU LOOP ---
    while True:
        clear_screen()
        print(f"Logged in as: {user_id}")
        print("-" * 30)
        print("1. 🔄 Sync All Secrets (Signatures + DB) from JSON")
        print("2. 🔍 Retrieve a Signature")
        print("3. 🔑 Get Database Credentials")
        print("4. 🚪 Exit")
        print("-" * 30)
        
        choice = input("Select Option (1-4): ").strip()

        if choice == '1':
            print("\n--- 🔄 SYNCING SECRETS FROM JSON ---")
            data = load_local_secrets()
            
            if data:
                # A. Sync Database Credentials
                if 'database' in data:
                    print("-> Updating Database Credentials...", end=" ")
                    success, msg = kmi.store_db_credentials(data['database'])
                    if success:
                        print("✅ Done")
                    else:
                        print(f"❌ Error: {msg}")
                else:
                    print("⚠️  No 'database' section found in JSON.")

                # B. Sync All Signatures
                if 'signatures' in data and isinstance(data['signatures'], list):
                    print(f"-> Found {len(data['signatures'])} signatures to upload:")
                    
                    for user_entry in data['signatures']:
                        target_user = user_entry.get('user_id')
                        sig_hash = user_entry.get('hash')
                        
                        if target_user and sig_hash:
                            print(f"   Uploading '{target_user}'...", end=" ")
                            success, msg = kmi.store_digital_signature(target_user, sig_hash)
                            if success:
                                print("✅")
                            else:
                                print(f"❌ ({msg})")
                        else:
                            print("   ⚠️  Skipping invalid entry (missing user_id or hash)")
                else:
                    print("⚠️  No 'signatures' list found in JSON.")
                    
                print("\n✨ Sync Complete!")
            else:
                print(f"❌ Error: Could not read {SECRETS_FILE}")
            
            input("[Press Enter to continue]")

        elif choice == '2':
            target_user = input("Enter User ID to lookup: ")
            sig_data, msg = kmi.get_digital_signature(target_user)
            if sig_data:
                print(f"✅ Found Signature: {sig_data}")
            else:
                print(f"⚠️  Result: {msg}")
            input("[Press Enter to continue]")

        elif choice == '3':
            print("Accessing Secure Storage...")
            db_creds = kmi.retrieve_db_credentials()
            if db_creds:
                print(f"💰 DB Credentials: {db_creds}")
            else:
                print("❌ Error: Could not retrieve credentials.")
            input("[Press Enter to continue]")

        elif choice == '4':
            print("Logging out...")
            sys.exit(0)

if __name__ == "__main__":
    main()