# group1-KMI-lab

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


