# src/api/services.py
"""
Servicios API simulados (sin dependencia de APIClient).
"""

def get_machine_status(machine_id: str) -> dict:
    """Simula el estado de una máquina."""
    return {
        "id": machine_id,
        "status": "Operativa",
        "temperature": 42,
        "last_maintenance": "2026-08-15"
    }

def get_all_machines() -> list:
    """Simula la lista de máquinas."""
    return [
        {"id": "M-101", "name": "Prensa hidráulica", "status": "Operativa"},
        {"id": "M-102", "name": "Cinta transportadora", "status": "Mantenimiento"},
        {"id": "M-103", "name": "Robot soldador", "status": "Operativa"}
    ]

def get_machine_maintenance_history(machine_id: str) -> list:
    """Simula el historial de mantenimiento."""
    return [
        {"date": "2026-08-15", "type": "Preventivo", "description": "Cambio de correas"},
        {"date": "2026-07-20", "type": "Correctivo", "description": "Reparación de motor"}
    ]