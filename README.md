# Group1-KMI-Lab

Project Task: Key Management Infrastructure (KMI)

A Key Management System (KMS) implementation using **HashiCorp Vault** and **Python**. This project demonstrates secure encryption key management, digital signature storage, and interoperability between team members using an "Infrastructure as Code" approach.

## Getting Started

Every developer runs their own local instance of the KMS. Follow these steps to set up your environment.

### 1. Prerequisites
* **Python 3.8+**
* **HashiCorp Vault** (Binary installed on your machine)

### 2. Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/hiterboy963/group1-KMI-lab.git
cd kmi-project
pip install hvac pyotp qrcode pillow
```

### 3. Start the KMS (Localhost)
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

### 5. Run the Application
Now that your local Vault is configured, you can run the main application logic.

```bash
python main.py
```

### How to update the progress?
We use Git to sync our progress because Hashivault is running on a local machine, not on the cloud. Here is the strict workflow to follow when adding new features.

### Scenario A: You want to add a new feature (e.g., MFA)
***Use this when you need a brand new "Folder" or "Shelf" in the Vault (e.g., adding MFA for the first time).***
you must update all 3 files:

1. Edit setup_vault.py: Add the code to create the new secret path.

Example:
```bash
client.secrets.kv.v2.create_or_update_secret(path='project/mfa', ...)
```
2. Edit kmi_client.py: Add a helper function so main.py can access it.

Example:
```bash
def get_mfa_secret(self):
    return ...
```

3. Edit main.py: Add the logic to actually use the new feature.

4. Commit & Push:

```bash
git add .
git commit
git push
```
### Scenario B: You are pulling the update
When a teammate pushes new code, you need to update your vault to sync the progress.

To get the Code:

```bash
git pull
```

To Update Your Infrastructure, Run the setup script again. This will create any new paths when added.

```bash
python setup_vault.py
python main.py
```
### Scenario C: You are just adding a Key (Data Entry)
*Use this when the "Folder" already exists, and you just want to put a new secret inside it. You do NOT need to touch the setup script.*

**Example:** The path `project/database` already exists, but you want to add a secondary password.

1.  **Edit `main.py` ONLY:**
    Use the client to write the new data to the existing path.
    ```python
    # We are just adding data to an existing path, so no setup_vault changes needed.
    kmi.client.secrets.kv.v2.create_or_update_secret(
        path='project/database',
        secret=dict(password="old-pass", backup_password="NEW-SECRET-HERE")
    )
    ```
2.  **Run `python main.py`** to test it.
3.  **Commit & Push `main.py`.**

## ⚠️ Understanding the Development Environment

It is important to understand that in this project, we are running HashiCorp Vault in **Development Mode** (`-dev`).

### How it works
1.  **In-Memory Storage:** The Vault server runs entirely in **RAM**. It does not write any data to your hard drive.
2.  **Volatile Data:** As soon as you stop the server (Ctrl+C) or close the terminal, **the Vault is destroyed.** All secrets, keys, and policies are wiped instantly.

### Why we use `setup_vault.py`
Because the Vault resets to a "blank slate" every time you restart it, we cannot rely on manual configuration. Instead, we use an **Infrastructure as Code (IaC)** approach:

* **The Server** (`vault server -dev`) provides the empty infrastructure.
* **The Script** (`setup_vault.py`) acts as the "Architect." When you run it, it programmatically rebuilds the entire environment—creating the secret paths, enabling audit logs, and setting up encryption keys from scratch.


