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
        print("1. Sync All Secrets (Signatures + Databases)")
        print("2. Retrieve a Signature")
        print("3. Get Database Credentials")
        print("4. Exit")
        print("-" * 30)
        
        choice = input("Select Option (1-4): ").strip()

        if choice == '1':
            print("\n--- 🔄 SYNCING SECRETS FROM JSON ---")
            data = load_local_secrets()
            
            if data:
                # A. Sync Database Credentials (LOOP)
                if 'database' in data and isinstance(data['database'], list):
                    print(f"-> Found {len(data['database'])} DB users to upload:")
                    for db_user in data['database']:
                        u_name = db_user.get('username')
                        if u_name:
                            print(f"   Uploading DB User '{u_name}'...", end=" ")
                            success, msg = kmi.store_db_credentials(u_name, db_user)
                            if success: print("✅")
                            else: print(f"❌ ({msg})")
                else:
                    print("⚠️  No 'database' list found in JSON.")

                # B. Sync Signatures (LOOP)
                if 'signatures' in data and isinstance(data['signatures'], list):
                    print(f"-> Found {len(data['signatures'])} signatures to upload:")
                    for user_entry in data['signatures']:
                        target = user_entry.get('user_id')
                        h = user_entry.get('hash')
                        if target and h:
                            print(f"   Uploading Signature '{target}'...", end=" ")
                            success, msg = kmi.store_digital_signature(target, h)
                            if success: print("✅")
                            else: print(f"❌ ({msg})")
                else:
                    print("⚠️  No 'signatures' list found in JSON.")
                    
                print("\n Sync Complete!")
            else:
                print(f"❌ Error: Could not read {SECRETS_FILE}")
            
            input("[Press Enter to continue]")

        elif choice == '2':
            # We still allow manual entry here so you can verify the storage worked
            target_user = input("Enter User ID to lookup: ")
            sig_data, msg = kmi.get_digital_signature(target_user)
            if sig_data:
                print(f"✅ Found Signature: {sig_data}")
            else:
                print(f"⚠️  Result: {msg}")
            input("[Press Enter to continue]")

        elif choice == '3':
            print("Accessing Secure Storage...")
            # Now we must ask WHICH database user to fetch
            target_db_user = input("Enter DB Username (e.g. db_admin, db_finance): ").strip()
            
            db_creds = kmi.retrieve_db_credentials(target_db_user)
            if db_creds:
                print(f"Credentials for {target_db_user}: {db_creds}")
            else:
                print(f"❌ Error: Could not find credentials for '{target_db_user}'.")
            input("[Press Enter to hide]")

        elif choice == '4':
            print("Logging out...")
            sys.exit(0)

if __name__ == "__main__":
    main()