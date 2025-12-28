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
pip install hvac
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
If you need to add a new secret (like an MFA key), you must update all 3 files:

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


