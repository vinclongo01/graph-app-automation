import sys
import os
import asyncio
import json

# Aggiunge la root del progetto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.graph_client import GraphClient 

# Utility function for serialization
def to_serializable(obj):
    """
    Try to convert an object to a dictionary recursively,
    skipping non-serializable attributes.
    """
    if isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return {key: to_serializable(value) for key, value in vars(obj).items() if not key.startswith("_")}
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        return str(obj)  # fallback to string


async def collect():
    """
    Instantiate applications from Microsoft Entra application templates.
    For each successfully instantiated application, retrieve the application and service principal information,
    and update two json files with all apps sp and app info.
    Finally delete the instatiated application.
    """

    client = GraphClient()


    #list of application objects
    all_applications = []
    #list of service principals list
    all_service_principals = []

    templates = await client.list_application_template()
    if templates:
        print(f"Successfully retrieved {len(templates)} application templates from Microsoft Entra.\n")
    else:
        print("No application templates found or failed to retrieve templates.\n")

    instantiated_apps = 0
    for i, template in enumerate(templates):
        id = template.get("id")
        display_name = template.get("display_name")

        try:
            print(f"Instantiating application from template {i + 1}/{len(templates)}: {id} - {display_name}")
            # Attempt to instantiate the application from the template
            app_info = await client.instantiate_application(id, display_name)
        except Exception as e:
            print(f"\tSkipping template {id} - {display_name}: error during instantiation\n")
            continue

        # If the app was succesfully instatiated
        if app_info:
            print(f"\tSuccessfully instantiated application from template {id} - {display_name}.")
            instantiated_apps += 1

            application_object = app_info["application"]
            service_principal = app_info["servicePrincipal"]

            serialized_application_object = to_serializable(application_object)
            serialized_service_principal = to_serializable(service_principal)

            all_applications.append(serialized_application_object)
            all_service_principals.append(serialized_service_principal)

            # Delete the instantiated application
            try:
                await client.delete_service_principal(service_principal.id)
                #print(f"Successfully deleted service principal {service_principal.id}\n")
            except Exception as e:
                print(f"\tError while removing service principal {service_principal.id}")

    instantiated_apps_percentage = (instantiated_apps / len(templates)) * 100 if templates else 0
    print(f"\nInstantiated Applications: {instantiated_apps} from {len(templates)} templates ({instantiated_apps_percentage:.2f}%).")
    # OUTPUT: Instantiated Applications: 1860 from 2870 templates (64.81%).

    return all_applications, all_service_principals

async def save_collections():
    all_applications, all_service_principals = await collect()

    with open("data/all_applications.json", "w", encoding="utf-8") as app_file:
        json.dump(all_applications, app_file, indent=2, ensure_ascii=False)

    with open("data/all_service_principals.json", "w", encoding="utf-8") as sp_file:
        json.dump(all_service_principals, sp_file, indent=2, ensure_ascii=False)
    

if __name__ == "__main__":
    asyncio.run(save_collections())


    print("\nEnd of Script.")

