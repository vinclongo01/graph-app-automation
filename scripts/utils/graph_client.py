import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.application_templates.application_templates_request_builder import ApplicationTemplatesRequestBuilder
from msgraph.generated.application_templates.item.instantiate.instantiate_post_request_body import InstantiatePostRequestBody



class GraphClient:

    def __init__(self):
        """
        Initialize the GraphClient instance.

        Loads environment variables from a .env file, sets up Azure identity credentials
        using ClientSecretCredential, and initializes the Microsoft GraphServiceClient
        for making authenticated requests to the Microsoft Graph API.

        Environment variables required:
        - TENANT_ID: Azure tenant ID
        - CLIENT_ID: Azure application (client) ID
        - CLIENT_SECRET: Azure application client secret

        The client is configured with the default Microsoft Graph scopes:
        'https://graph.microsoft.com/.default'. (i.e., the scopes defined in the MS Entra ID App registration)
        """

        # Load environment variables from .env file
        load_dotenv()

        # credentials for the GraphServiceClient
        self.credential = ClientSecretCredential(
            tenant_id=os.getenv("TENANT_ID"),
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET")
        )

        # scopes for the GraphServiceClient
        self.scopes = ['https://graph.microsoft.com/.default']  # in this way we can use the default scopes: i.e. the scopes defined in the MS Entra ID App registration

        # the client application to interact with Microsoft Graph API
        self.client = GraphServiceClient(credentials=self.credential, scopes=self.scopes)

    async def list_application_template(self, select_fields: list = None):
        """
        Retrieve the list of available application templates from Microsoft Entra App Gallery.

        HTTP method: GET
        Endpoint: /applicationTemplates

        Args:
            select_fields (list, optional): List of fields to include in the output dictionaries.
                Defaults to ['id', 'displayName'].

        Returns:
            list of dict: List of application templates with only the selected fields included.
        """

        if select_fields is None:
            select_fields = ["id", "displayName"]

        try:
            # Simple GET request without query parameters
            result = await self.client.application_templates.get()

            # Return only selected fields (post-filtering)
            return [
                {
                    field.strip(): getattr(template, field.strip(), None)
                    for field in select_fields
                }
                for template in result.value
            ] if result and result.value else []
        except Exception as e:
            print(f"Error retrieving application templates: {e}")
            return []

    async def instantiate_application(self, template_id: str, display_name: str, select_fields_sp: list = None, select_fields_app: list = None):
        """
        Instantiate a new application from a given application template in Microsoft Entra.

        HTTP method: POST
        Endpoint: /applicationTemplates/{template_id}/instantiate

        Args:
            template_id (str): The ID of the application template to instantiate.
            display_name (str): The display name to assign to the new application.
            select_fields_sp (list, optional): List of fields to include from the servicePrincipal object.
                Defaults to ['id', 'appId', 'displayName'].
            select_fields_app (list, optional): List of fields to include from the application object.
                Defaults to ['id', 'appId', 'displayName'].

        Returns:
            dict or None: A dictionary containing filtered 'servicePrincipal' and 'application' objects
                with only the selected fields, or None if instantiation fails.
        """

        try:
            request_body = InstantiatePostRequestBody(
                display_name=display_name,
            )
            result = await self.client.application_templates.by_application_template_id(template_id).instantiate.post(request_body)

            if not result or not result.value:
                return None

            # Important Note: The result is a complete object with both application and servicePrincipal objects of the instantiated application.
            # So we can directly access all information from the result (e.g. delegatedPermissions from oauth2PermissionScopes in the servicePrincipal object).
            # Return only selected fields (post-filtering)

            data = result.value
            # Extract ServicePrincipal object from the result
            servicePrincipal = data.get('servicePrincipal', {})
            # Extract Application object from the result
            application = data.get('application', {})

            if len(servicePrincipal) == 0 or len(application) == 0:
                return None
            
            # Filter only selected fields from the servicePrincipal and application objects
            # filter function to filter fields from the servicePrincipal and application objects
            def filter_fields(obj: dict, fields: list):
                return {field.strip(): obj.get(field.strip()) for field in fields} if fields > 0 else obj # if fields is empty, return the whole object
            

            # If fields are specified, filter the objects otherwise return the whole object
            return {
                "servicePrincipal": filter_fields(servicePrincipal, select_fields_sp),
                "application": filter_fields(application, select_fields_app)
            }

        except Exception as e:
            print(f"Error instantiating application from template {template_id}: {e}")
            return None

    async def get_service_principal(self, service_principal_id: str):
        """
        Retrieve detailed information about a specific Service Principal by its ID.

        HTTP method: GET
        Endpoint: /servicePrincipals/{service_principal_id}

        Args:
            service_principal_id (str): The unique identifier of the Service Principal.

        Returns:
            dict or None: The Service Principal object as a dictionary if found, else None.
        """
        pass

    async def get_oauth2_permission_grants(self, service_principal_id: str):
        """
        Retrieve the OAuth2 permission grants associated with a specific Service Principal.

        HTTP method: GET
        Endpoint: /oauth2PermissionGrants

        Args:
            service_principal_id (str): The unique identifier of the Service Principal.

        Returns:
            list or None: A list of OAuth2 permission grant objects if any exist, else None.
        """
        pass

    async def delete_service_principal(self, service_principal_id: str):
        """
        Delete a specific Service Principal by its ID.

        HTTP method: DELETE
        Endpoint: /servicePrincipals/{service_principal_id}

        Args:
            service_principal_id (str): The unique identifier of the Service Principal to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """

        try:
            await self.client.service_principals.by_service_principal_id(service_principal_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting Service Principal {service_principal_id}: {e}")
            return False
