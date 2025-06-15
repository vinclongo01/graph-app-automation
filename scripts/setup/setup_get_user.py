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

    users = await client.get_users(["id", "displayName"])
    if users:
        print(f"Successfully retrieved {len(users)} users from Microsoft Entra.")
        for user in users:
            print(f"User ID: {user['id']}, Display Name: {user['displayName']}")
    else:
        print("No users found or failed to retrieve users.")

if __name__ == "__main__":
    asyncio.run(setup())
    print("Setup completed.")

