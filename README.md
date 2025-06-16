# App Deployment Automation with Microsoft Graph API

## Description

This project automates the deployment and analysis of applications from the **Microsoft Entra App Gallery** using the **Microsoft Graph API**.

It provides asynchronous utilities to:

* Retrieve application templates
* Instantiate applications from templates
* Collect and save metadata (applications and service principals)
* Delete the created service principals after collection

---

## Project Structure

```
.
├── data/
│   ├── all_applications.json            # Saved application metadata
│   └── all_service_principals.json      # Saved service principal metadata
│
├── scripts/
│   ├── apps/
│   │   └── collect.py                   # Collects application and SP metadata from Entra templates
│   ├── auth/                            # (Authentication-related scripts, if applicable)
│   ├── setup/
│   │   ├── setup_get_app_templates.py
│   │   ├── setup_get_user.py
│   │   └── setup_instantiate_app.py
│   └── users/
│
├── utils/
│   ├── __init__.py
│   └── graph_client.py                  # GraphClient class (handles Graph API calls)
│
├── .env                                 # Environment variables (tenant/client IDs and secret)
├── requirements.txt                     # Python dependencies
├── LICENSE
└── README.md                            # Project documentation
```

---

## Setup Instructions

### 1. Create a `.env` file in the root directory with the following content:

```
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id <- the if of you client application created within your Microsoft Entra ID tenant
CLIENT_SECRET=your-client-secret <- the secret that your application uses to authenticate itself inside the tenant
```

### Installation

Make sure you have **Python 3.8 or higher** installed. This project uses asynchronous requests to interact with the Microsoft Graph API.

To install the core dependencies, please refer to the official Microsoft Graph SDK for Python documentation:

**link** -> [https://github.com/microsoftgraph/msgraph-sdk-python](https://github.com/microsoftgraph/msgraph-sdk-python)

In particular, you can install the asynchronous Graph SDK with:

```bash
pip install msgraph-sdk
```

Note: This project also uses python-dotenv to manage environment variables from a .env file.
You can install it with:

```bash
pip install python-dotenv
```

---

## Running the Collection Script

The `scripts/apps/collect.py` script:

* Iterates over **Microsoft Entra application** templates
* Instantiates an application from each template
* Collects metadata for each application and its corresponding service principal
* Saves the results in `data/all_applications.json` and `data/all_service_principals.json`
* Deletes the service principals to avoid clutter

### Set-up

Some set-up scripts are available for testing your `GraphClient`.

### To run:

```bash
python scripts/apps/collect.py
```

After completion, the collected data will be available under the `data/` directory.

---

## Requirements

* Python 3.8 or higher
* Microsoft Entra ID App Registration with sufficient Graph API permissions:

  * `Application.ReadWrite.All`
  * `ApplicationTemplate.Read.All`
  * `ServicePrincipal.ReadWrite.All`

---

## Next Steps

* Analyze the permissions of instantiated applications
* Export and transform data to CSV or DataFrames
* Define rules to classify applications as **benign** or **malicious** based on permission sets
* Integrate with Microsoft Sentinel for threat correlation

---

## Notes

The project is modular and structured for extension. You can reuse the `GraphClient` in other scripts (e.g., for audit logs or user analysis).

---


