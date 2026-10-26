# src/api/services.py


# Defines get_machine_status to get the current status of a machine from the API server.
#         Sends a GET request to the machine endpoint.

# Defines get_all_machines to get the list of all machines from the API server.
#         Sends a GET request to the machines endpoint.

# Defines get_machine_maintenance_history to get the maintenance history of a machine from the API server.
#         Sends a GET request to the machine maintenance endpoint.


from src.api.client import APIClient


api_client = APIClient()


# Defines get_machine_status to get the current status of a machine from the API server.
def get_machine_status(machine_id: str) -> dict:

    # Sends a GET request to the machine endpoint.
    return api_client.get(f"/machines/{machine_id}")


# Defines get_all_machines to get the list of all machines from the API server.
def get_all_machines() -> list:

    # Sends a GET request to the machines endpoint.
    return api_client.get("/machines")


# Defines get_machine_maintenance_history to get the maintenance history of a machine from the API server.
def get_machine_maintenance_history(machine_id: str) -> list:

    # Sends a GET request to the machine maintenance endpoint.
    return api_client.get(f"/machines/{machine_id}/maintenance")
