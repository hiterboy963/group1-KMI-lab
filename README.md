# Group1-KMI-Lab

Project Task: Key Management Infrastructure (KMI)

A Key Management System (KMS) implementation using **HashiCorp Vault** and **Python**. This project demonstrates secure encryption key management, digital signature storage, and interoperability between team members using an "Infrastructure as Code" approach.

## Features
* **Secure Storage:** Uses HashiCorp Vault to store database credentials and digital signatures.
* **MFA Protection:** Application-level Multi-Factor Authentication (TOTP) using `pyotp`.
* **No Hardcoded Secrets:** All sensitive data is loaded from a local `secrets.json` file.
* **Interactive CLI:** A secure menu system to sync, retrieve, and manage secrets.

---

## Getting Started

Every developer runs their own local instance of the KMS. Follow these steps to set up your environment.

### 1. Prerequisites
* **Python 3.8+**
* **HashiCorp Vault** (Binary installed on your machine)

### How to install HashiCorp Vault?

Before running the given Python scripts, you must have the Vault binary installed and accessible in your system PATH.

#### On Windows:

1. Download the Windows binary from the HashiCorp Downloads Page: https://developer.hashicorp.com/vault/install

2. Unzip the downloaded file (you will find vault.exe).

3. Move vault.exe to a folder (e.g., C:\Vault).

4. Add that folder to your System Environment Variables (PATH).

### On macOS:

1. Download the Binary by going to the HashiCorp Downloads Page.

2. Click on the latest version (e.g., 1.15.x).

3. Scroll down to the macOS section.

4. Download the correct zip file for your chip:

- Intel Macs: vault_x.x.x_darwin_amd64.zip

- M1/M2/M3 Macs: vault_x.x.x_darwin_arm64.zip

5. Unzip the File
Open your terminal, navigate to your Downloads folder, and unzip the file.


6. Unquarantine the Binary (Crucial)
If you try to run vault now, macOS will likely block it with a "Developer cannot be verified" error. Run this command to whitelist it:

```bash
sudo xattr -d com.apple.quarantine /usr/local/bin/vault
```
### On Linux(Ubuntu/Debian):

```bash
wget -O- [https://apt.releases.hashicorp.com/gpg](https://apt.releases.hashicorp.com/gpg) | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] [https://apt.releases.hashicorp.com](https://apt.releases.hashicorp.com) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault
```
### 2. Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/hiterboy963/group1-KMI-lab.git
# Upgrade pip and install requirements
cd group1-KMI-lab
pip install --upgrade pip
pip install -r requirements.txt
```
### 3. Setup Configuration (Secrets File)

You must create a local configuration file.

Create a file named secrets.json in the project root.

Paste the following template and fill in your own test data:
```JSON
{
    "database": [
        {
            "username": "db_admin",
            "password": "super-secure-db-password-999"
        },
        {
            "username": "db_finance",
            "password": "finance-secure-password-111"
        }
    ],
    "signatures": [
        {
            "user_id": "student_01",
            "hash": "a1b2-c3d4-e5f6-secure-hash-01"
        },
        {
            "user_id": "student_02",
            "hash": "x9y8-z7w6-v5u4-secure-hash-02"
        }
    ]
}
```

### 4. Start the KMS (Localhost)
Open a terminal and start the Vault server in development mode:

```bash
vault server -dev
```


⚠️ IMPORTANT

Do not close this terminal window

Copy the Root Token from the output (it starts with hvs...)

You will need this token in the next step

### 4️. Seed Your Local Vault

We use a setup script to ensure everyone has the same secret paths. Examples: secret paths (Database, Signatures, etc.).

Run the following command:

```bash
python setup_vault.py
```

When prompted, paste the Root Token you copied from Step 3.

### 5. Enroll in MFA (First Time Only)
You cannot use the main application until you enroll your user identity.

```bash
python enroll_mfa.py
```
1. Enter your User ID (e.g., student_01).

2. Scan the generated QR code with Google Authenticator (or Authy).

3. Verify the 6-digit code to complete enrollment.

### 5. Run the Application
Now that your local Vault is configured, you can run the main application logic.

```bash
python main_mfa.py
```
Login: Enter your User ID, Vault Token, and the 6-digit MFA code from your phone.

- Menu Options:

1. Option 1 (Sync): Reads secrets.json and pushes all signatures and DB credentials to Vault.

2. Option 2 (Retrieve Signature): Fetches a specific user's hash from Vault.

3. Option 3 (Get DB Password): Asks for a DB username (e.g., db_admin) and reveals the credentials.

---

### How to update the progress?
Edit the parameters in the secrets.json file.

## ⚠️ Understanding the Development Environment

It is important to understand that in this project, we are running HashiCorp Vault in **Development Mode** (`-dev`).

### How it works
1.  **In-Memory Storage:** The Vault server runs entirely in **RAM**. It does not write any data to your hard drive.
2.  **Volatile Data:** As soon as you stop the server (Ctrl+C) or close the terminal, **the Vault is destroyed.** All secrets, keys, and policies are wiped instantly.

### Why we use `setup_vault.py`
Because the Vault resets to a "blank slate" every time you restart it, we cannot rely on manual configuration. Instead, we use an **Infrastructure as Code (IaC)** approach:

* **The Server** (`vault server -dev`) provides the empty infrastructure.
* **The Script** (`setup_vault.py`) acts as the "Architect." When you run it, it programmatically rebuilds the entire environment—creating the secret paths, enabling audit logs, and setting up encryption keys from scratch.


