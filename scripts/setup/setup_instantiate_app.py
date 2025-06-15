import sys
import os
import asyncio
import json

# Aggiunge la root del progetto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.graph_client import GraphClient 


# Utility function to print application and service principal information
def print_app_and_sp_info(app_info):
    application = app_info.get("application")
    sp = app_info.get("servicePrincipal")

    if application:
        print("\n=== APPLICATION INFO ===")
        print(f"Display Name: {application.display_name}")
        print(f"App ID: {application.app_id}")
        print(f"Object ID: {application.id}")
        print(f"Created At: {application.created_date_time}")
        print(f"Sign-in Audience: {application.sign_in_audience}")
        print(f"Publisher Domain: {application.publisher_domain}")

        if application.info:
            print("\n--- Informational URLs ---")
            homepage = getattr(application.info, "home_page_url", None) or getattr(application.info, "homepage", None)
            if homepage:
                print(f"Home Page: {homepage}")
            privacy_url = getattr(application.info, "privacy_statement_url", None)
            if privacy_url:
                print(f"Privacy URL: {privacy_url}")
            support_url = getattr(application.info, "support_url", None)
            if support_url:
                print(f"Support URL: {support_url}")
            tos_url = getattr(application.info, "terms_of_service_url", None)
            if tos_url:
                print(f"Terms of Service URL: {tos_url}")

        if application.web:
            print("\n--- Web Application ---")
            homepage_web = getattr(application.web, "home_page_url", None) or getattr(application.web, "homepage", None)
            if homepage_web:
                print(f"Home Page URL: {homepage_web}")
            redirect_uris = getattr(application.web, "redirect_uris", [])
            if redirect_uris:
                print(f"Redirect URIs: {redirect_uris}")

        if application.app_roles:
            print("\n--- App Roles ---")
            for role in application.app_roles:
                print(f"- {role.display_name} (ID: {role.id}, Enabled: {role.is_enabled})")

        if application.api and application.api.oauth2_permission_scopes:
            print("\n--- OAuth2 Permission Scopes ---")
            for scope in application.api.oauth2_permission_scopes:
                print(f"- {scope.user_consent_display_name} ({scope.value})")

        if len(application.required_resource_access) > 0:
            print("\n--- Required Resource Access ---")
            for resource in application.required_resource_access:
                print(f"Resource App ID: {resource.resource_app_id}")
                for scope in resource.resource_access:
                    print(f"- {scope.value} (Type: {scope.type})")
        else:
            print("\n--- Required Resource Access field empty ---")


    if sp:
        print("\n=== SERVICE PRINCIPAL INFO ===")
        print(f"Display Name: {sp.display_name}")
        print(f"Object ID: {sp.id}")
        print(f"App ID: {sp.app_id}")
        print(f"Service Principal Type: {sp.service_principal_type}")
        print(f"Account Enabled: {sp.account_enabled}")
        print(f"Homepage: {sp.homepage}")
        print(f"Reply URLs: {sp.reply_urls}")
        print(f"Tags: {sp.tags}")

        if sp.app_roles:
            print("\n--- App Roles (Service Principal) ---")
            for role in sp.app_roles:
                print(f"- {role.display_name} (ID: {role.id}, Enabled: {role.is_enabled})")

        if sp.oauth2_permission_scopes:
            print("\n--- OAuth2 Permission Scopes (Service Principal) ---")
            for scope in sp.oauth2_permission_scopes:
                print(f"- {scope.user_consent_display_name} ({scope.value})")

    print("\n=========================\n")




async def setup():
    """
    Setup the graph client and test the connection to Microsoft Entra
    by retrieving the list of users.
    """


    client = GraphClient()

    templates = await client.list_application_template()
    if templates:
        print(f"Successfully retrieved {len(templates)} application templates from Microsoft Entra.")
    else:
        print("No application templates found or failed to retrieve templates.")

    for i, template in enumerate(templates):
        id = template.get("id")
        display_name = template.get("display_name")

        try:
            print(f"Instantiating application from template {i + 1}/{len(templates)}: {id} - {display_name}")
            # Attempt to instantiate the application from the template
            app_info = await client.instantiate_application(id, display_name)
        except Exception as e:
            print(f"Skipping template {id} - {display_name}: {e}")
            continue

        if app_info:
            print(f"Successfully instantiated application from template {id} - {display_name}.")

            print_app_and_sp_info(app_info)
            break

if __name__ == "__main__":
    asyncio.run(setup())
    print("End of Script.")

