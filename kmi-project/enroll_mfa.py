#!/usr/bin/env python3

# MFA Enrollment Script for KMI Users
# Run this to enroll a new user in MFA and generate their QR code.

from mfa_auth import MFAManager
import sys

def main():
    print("=" * 50)
    print("  KMI MFA ENROLLMENT")
    print("=" * 50)
    print()
    
    mfa = MFAManager()
    
    user_id = input("Enter User ID to enroll: ").strip()
    
    if not user_id:
        sys.exit("Error: User ID cannot be empty")
    
    if mfa.is_enrolled(user_id):
        print(f"\nWarning: User '{user_id}' is already enrolled in MFA.")
        choice = input("Re-enroll? This will invalidate the old secret. (y/N): ").strip().lower()
        if choice != 'y':
            sys.exit("Enrollment cancelled.")
        mfa.remove_user(user_id)
    
    # Enroll the user
    secret, uri = mfa.enroll_user(user_id)
    
    print()
    print("✓ MFA Enrollment Successful!")
    print("-" * 50)
    print()
    print("OPTION 1: Scan QR Code")
    print("  Generating QR code...")
    
    qr_path = mfa.generate_qr_code(uri, f"mfa_qr_{user_id}.png")
    print(f"  QR Code saved to: {qr_path}")
    print("  Scan this with Google Authenticator, Authy, or similar app.")
    print()
    print("OPTION 2: Manual Entry")
    print(f"  Secret Key: {secret}")
    print("  (Enter this manually in your authenticator app)")
    print()
    print("-" * 50)
    
    # Verification test
    print("Let's verify your setup:")
    test_code = input("Enter the 6-digit code from your authenticator app: ").strip()
    
    if mfa.verify_totp(user_id, test_code):
        print()
        print("✔ MFA VERIFIED SUCCESSFULLY!")
        print(f"  User '{user_id}' is now protected with MFA.")
        print()
        print("IMPORTANT: Keep your authenticator app secure!")
        print("  If you lose access, you'll need admin help to re-enroll.")
    else:
        print()
        print("✘ Verification failed!")
        print("  The code was incorrect or expired.")
        print("  Please try enrollment again.")
        mfa.remove_user(user_id)
        sys.exit(1)


if __name__ == "__main__":
    main()
