import hvac
import sys
import json

SECRETS_FILE = 'secrets.json'

def configure_local_vault():
    print("--- INITIALIZING KMI INFRASTRUCTURE ---")
    
    # 1. Load Secrets
    try:
        with open(SECRETS_FILE, 'r') as f:
            config_data = json.load(f)
            print(f"✓ Configuration loaded from {SECRETS_FILE}")
    except FileNotFoundError:
        sys.exit(f"❌ Error: {SECRETS_FILE} not found.")

    # 2. Connect
    client = hvac.Client(url='http://127.0.0.1:8200')
    
    if not client.is_authenticated():
        token = input("Enter Root Token: ")
        client.token = token

    if not client.is_authenticated():
        sys.exit("❌ Authentication Failed.")

    # 3. Configure Database Secrets (LOOP)
    print("...Configuring 'project/database'...")
    
    # Create the parent folder first
    client.secrets.kv.v2.create_or_update_secret(
        path='project/database/config',
        secret=dict(status="active")
    )

    if 'database' in config_data and isinstance(config_data['database'], list):
        for db_user in config_data['database']:
            u_name = db_user['username']
            u_pass = db_user['password']
            
            print(f"   -> Uploading credentials for: {u_name}")
            client.secrets.kv.v2.create_or_update_secret(
                path=f'project/database/{u_name}',
                secret=dict(username=u_name, password=u_pass)
            )
    else:
        print("   ⚠️  Warning: 'database' section in JSON is missing or not a list.")

    # 4. Configure Signatures (LOOP)
    print("...Configuring 'project/signatures'...")
    client.secrets.kv.v2.create_or_update_secret(
        path='project/signatures/config',
        secret=dict(status="active")
    )

    if 'signatures' in config_data:
        for user_entry in config_data['signatures']:
            uid = user_entry['user_id']
            sig = user_entry['hash']
            print(f"   -> Pre-loading signature for '{uid}'")
            
            client.secrets.kv.v2.create_or_update_secret(
                path=f'project/signatures/{uid}',
                secret=dict(hash=sig)
            )
    
    print("✅ INFRASTRUCTURE READY")

if __name__ == "__main__":
    configure_local_vault()