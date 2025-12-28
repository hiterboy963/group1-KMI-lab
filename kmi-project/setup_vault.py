import hvac
import sys

def configure_local_vault():
    print("--- INITIALIZING KMI INFRASTRUCTURE ---")
    
    # 1. Connect to the local Vault instance
    client = hvac.Client(url='http://127.0.0.1:8200')
    
    # 2. Authentication Check
    if not client.is_authenticated():
        # Input token manually if not detected automatically
        token = input("Enter Root Token to configure infrastructure: ")
        client.token = token

    if not client.is_authenticated():
        sys.exit("❌ Authentication Failed. Cannot configure Vault.")

    # 3. Create 'Database' Secret Path
    # Defines the storage for database credentials
    print("...Configuring path 'project/database'...")
    client.secrets.kv.v2.create_or_update_secret(
        path='project/database',
        secret=dict(password="dev-db-password-123") 
    )

    # 4. Create 'Signatures' Secret Path
    # Defines the storage for user digital signatures
    print("...Configuring path 'project/signatures'...")
    client.secrets.kv.v2.create_or_update_secret(
        path='project/signatures/config',
        secret=dict(status="active")
    )

    print(" INFRASTRUCTURE READY: Secret paths configured successfully.")

if __name__ == "__main__":
    configure_local_vault()