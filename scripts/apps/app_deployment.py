import asyncio
from utils.graph_client import GraphClient


async def get_template_ids(client: GraphClient):
    """
    Retrieve the list of available application templates from Microsoft Entra App Gallery.

    Args:
        client (GraphClient): An instance of the GraphClient.

    Returns:
        list: List of application template IDs.
    """
    templates = await client.list_application_template(["id"])
    return [(template['id'], template['displayName']) for template in templates]

async def get_app_info(client: GraphClient, template_id: str, display_name: str):
    """
    Instantiate a new application from a given application template in Microsoft Entra.

    Args:
        client (GraphClient): An instance of the GraphClient.
        template_id (str): The ID of the application template to instantiate.
        display_name (str): The display name to assign to the new application.

    Returns:
        dict: A dictionary containing filtered 'servicePrincipal' and 'application' objects
              with only the selected fields.
    """
    result = await client.instantiate_application(template_id, display_name, None, None) # return the whole service principal and application objects

    if not result:
        print(f"Failed to instantiate application from template {template_id}.")
        return None

    # remove the servicePrincipal from the tenant
    service_principal_id = result['servicePrincipal']['id']
    if await client.delete_service_principal(service_principal_id):
        print(f"Service Principal {service_principal_id} deleted successfully.")
    else:
        print(f"Failed to delete Service Principal {service_principal_id}.")
    
    return result

async def main():
    """
    Main entry point for the application deployment script.
    An asynchronous function that retrieves application templates,
    instantiates applications from those templates, and collects their information.
    It prints the total number of applications instantiated at the end.
    """

    client = GraphClient()

    template_ids = await get_template_ids(client)

    # Initialize the list of dictionaries to store the app_info of each instantiated application
    app_info_list = []

    if not template_ids:
        print("No application templates found.")
    else:
        print("Available application templates:")
        for template_id, display_name in template_ids:
            print(f"- {template_id}: {display_name}")
            
            display_name_sp = f"{display_name} Service Principal"

            print(f"Instantiating application template {template_id} with display name '{display_name_sp}'...")
            app_info = await get_app_info(client, template_id, display_name_sp)
            if app_info:
                print(f"Application instantiated successfully: {app_info['application']['id']}")
                # Append the app_info to the list
                app_info_list.append(app_info)
            else:
                print("Failed to instantiate application.")

    # Do something with the app_info_list
    print(f"Total applications instantiated: {len(app_info_list)}")


if __name__ == "__main__":
    asyncio.run(main())