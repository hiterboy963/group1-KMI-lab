from kmi_client import KMIClient
import sys

# --- CONFIGURATION ---
USER_TOKEN = input("Please enter your Vault Token: ")

def main():
    print("--- KMI APPLICATION START ---")

    # 1. Initialize the Client
    kmi = KMIClient(token=USER_TOKEN)
    
    if not kmi.is_connected:
        sys.exit("❌ Fatal Error: Could not authenticate with KMI.")

    # 2. FEATURE IMPLEMENTATION: Digital Signatures
    # Simulating an example of a user student_01 signature generation
    current_user = "student_01"
    signature_data = "a1b2-c3d4-e5f6-secure-hash"
    
    print(f"Processing signature for user: {current_user}...")
    success, msg = kmi.store_digital_signature(current_user, signature_data)
    
    if success:
        print(f" SUCCESS: {msg}")
    else:
        print(f" ERROR: {msg}")

    # 3. FEATURE IMPLEMENTATION: Credential Retrieval
    print("Requesting database access...")
    db_pass = kmi.retrieve_db_credentials()
    
    if db_pass:
        print(f" Access Granted. DB Password: {db_pass}")
    else:
        print(" Access Denied: Could not retrieve credentials.")

if __name__ == "__main__":
    main()