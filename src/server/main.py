from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Machine Management API",
    description="REST API for machine data",
    version="1.0.0"
)


machines = {
    "M-101": {
        "id": "M-101",
        "name": "Prensa hidráulica",
        "status": "Operativa",
        "temperature": 38,
        "last_maintenance": "2026-08-10"
    },
    "M-102": {
        "id": "M-102",
        "name": "Cinta transportadora",
        "status": "Mantenimiento",
        "temperature": 42,
        "last_maintenance": "2026-08-15"
    },
    "M-103": {
        "id": "M-103",
        "name": "Robot soldador",
        "status": "Operativa",
        "temperature": 45,
        "last_maintenance": "2026-08-20"
    }
}


@app.get("/machines")
def get_all_machines():
    """Return all machines."""
    return list(machines.values())


@app.get("/machines/{machine_id}")
def get_machine(machine_id: str):
    """Return information about one machine."""

    if machine_id not in machines:
        raise HTTPException(
            status_code=404,
            detail=f"Machine {machine_id} not found"
        )

    return machines[machine_id]