import hvac

class KMIClient:
    def __init__(self, token, url='http://127.0.0.1:8200'):
        """Initialize connection to the Key Management Infrastructure."""
        self.client = hvac.Client(url=url, token=token)
        self.is_connected = self.client.is_authenticated()

    def store_digital_signature(self, user_id, signature_hash):
        """Securely stores a digital signature hash for a specific user."""
        if not self.is_connected:
            return False, "Not Connected"

        try:
            # We map the user_id to a specific secret path
            secret_path = f"project/signatures/{user_id}"
            
            self.client.secrets.kv.v2.create_or_update_secret(
                path=secret_path,
                secret=dict(hash=signature_hash)
            )
            return True, "Signature Stored"
        except Exception as e:
            return False, str(e)

    def retrieve_db_credentials(self):
        """Retrieves the database password for application access."""
        if not self.is_connected:
            return None
            
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path='project/database')
            return response['data']['data']['password']
        except Exception:
            return None