import hvac
import sys
import json

SECRETS_FILE = 'secrets.json'

def configure_local_vault():
    print("--- INITIALIZING KMI INFRASTRUCTURE ---")
    
    # 1. Load Secrets from JSON
    try:
        with open(SECRETS_FILE, 'r') as f:
            config_data = json.load(f)
            print(f"✓ Configuration loaded from {SECRETS_FILE}")
    except FileNotFoundError:
        sys.exit(f"❌ Error: {SECRETS_FILE} not found.")

    # 2. Connect to the local Vault instance
    client = hvac.Client(url='http://127.0.0.1:8200')
    
    # 3. Authentication Check
    if not client.is_authenticated():
        token = input("Enter Root Token: ")
        client.token = token

    if not client.is_authenticated():
        sys.exit("❌ Authentication Failed.")

    # 4. Create 'Database' Secret Path
    # Defines the storage for database credentials
    print("...Configuring 'project/database'...")
    # Updated to store the entire dictionary (username + password)
    client.secrets.kv.v2.create_or_update_secret(
        path='project/database',
        secret=config_data['database'] 
    )

    # 5. Create 'Signatures' Secret Path
    # Defines the storage for user digital signatures
    print("...Configuring 'project/signatures'...")
    
    # Create the parent config path first
    client.secrets.kv.v2.create_or_update_secret(
        path='project/signatures/config',
        secret=dict(status="active")
    )
    
    # Loop through the list of users in JSON and create secrets for each
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