import sys
import os
import asyncio

# Aggiunge la root del progetto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.graph_client import GraphClient 

async def setup():
    """
    Setup the graph client and test the connection to Microsoft Entra
    by retrieving the list of users.
    """


    client = GraphClient()

    templates = await client.list_application_template()
    if templates:
        print(f"Successfully retrieved {len(templates)} application templates from Microsoft Entra.")
        to_print = 10
        print(f"Displaying the first {to_print} templates:")
        for template in templates[:to_print]:
            # Print only the first 10 templates for brevity
            print(f"Template ID: {template['id']}, Display Name: {template['display_name']}")
    else:
        print("No application templates found or failed to retrieve templates.")

if __name__ == "__main__":
    asyncio.run(setup())
    print("Setup completed.")

