# App Deployment Automation with Microsoft Graph API

**Description**  
This project automates the deployment of applications from the **Microsoft Entra App Gallery** using the **Microsoft Graph API**. 
It retrieves all available application templates, instantiates applications from them, and removes the associated Service Principals after creation.

**Project Structure**  
- `scripts/app_deployment.py`  
  Asynchronous script that:
  - Retrieves application templates
  - Instantiates applications from each template
  - Deletes their associated Service Principals
  - Collects and stores relevant application information

- `utils/graph_client.py`  
  Contains the `GraphClient` class, an asynchronous *wrapper* around **Microsoft Graph API** operations.

**Setup Instructions**  
1. Create a `.env` file with the following variables:
    `TENANT_ID`=your-tenant-id
    `CLIENT_ID`=your-client-id
    `CLIENT_SECRET`=your-client-secret

2. Install dependencies:

```bash
python scripts/app_deployment.py
```

3. Run the script `python scripts/app_deployment.py`

**Requirements**  
- **Python 3.8** or higher  
- **Microsoft Entra ID App Registration** with necessary **Graph API permissions**

**Next Steps**  
- Analyze the permissions of instantiated applications  
- Export data to JSON or CSV  
- Develop rules to classify applications as benign or malicious based on permission sets

