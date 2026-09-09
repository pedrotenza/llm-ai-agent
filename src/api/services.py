# src/api/services.py
"""
Servicios API que utilizan el cliente HTTP para comunicarse con el servidor FastAPI.
"""

from src.api.client import APIClient

# Instancia global del cliente (usa la URL desde config por defecto)
api_client = APIClient()


def get_machine_status(machine_id: str) -> dict:
    """
    Obtiene el estado actual de una máquina desde el servidor.

    Args:
        machine_id (str): Identificador de la máquina.

    Returns:
        dict: Respuesta de la API (puede contener "error" si falla).
    """
    return api_client.get(f"/machines/{machine_id}")


def get_all_machines() -> list:
    """
    Obtiene el listado de todas las máquinas.

    Returns:
        list: Lista de máquinas o dict con error.
    """
    return api_client.get("/machines")


def get_machine_maintenance_history(machine_id: str) -> list:
    """
    Obtiene el historial de mantenimiento de una máquina.

    Args:
        machine_id (str): Identificador de la máquina.

    Returns:
        list: Historial de mantenimientos o dict con error.
    """
    return api_client.get(f"/machines/{machine_id}/maintenance")