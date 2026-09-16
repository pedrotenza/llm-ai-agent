# src/agent/tools.py
"""
Herramientas que el agente puede utilizar para interactuar con el sistema.
Cada herramienta recibe parámetros simples y devuelve un string legible.
"""

from src.rag.rag_pipeline import retrieve_information
from src.api.services import get_machine_status, get_all_machines


def search_documents(question: str) -> str:
    """
    Busca información en los documentos PDF (manuales, normativas, procedimientos).
    Úsalo cuando el usuario pregunte sobre reglas, pasos a seguir, o descripciones
    que puedan estar en los manuales.

    Args:
        question (str): La pregunta del usuario.

    Returns:
        str: Fragmentos relevantes formateados o mensaje de error.
    """
    try:
        # Suponemos que retrieve_information devuelve una lista de dicts con 'text' y 'source'
        results = retrieve_information(question, k=3)
        if not results:
            return "No encontré información relevante en los documentos."

        # Formateamos para que el LLM entienda las fuentes (incluyendo la página)
        context = "\n\n".join([
            f"Fuente: {r.get('source', 'desconocida')} (página {r.get('page', '?')})\nTexto: {r['text']}"
            for r in results
        ])
        return f"Información extraída de los documentos:\n{context}"
    except Exception as e:
        return f"Error al buscar en documentos: {str(e)}"


def get_machine_api_status(machine_id: str) -> str:
    """
    Obtiene el estado en tiempo real de una máquina específica (temperatura,
    estado operativo, última fecha de mantenimiento, etc.).

    Args:
        machine_id (str): Identificador de la máquina (ej. "M-101").

    Returns:
        str: Información detallada de la máquina o mensaje de error.
    """
    data = get_machine_status(machine_id)
    if isinstance(data, dict) and "error" in data:
        return f"No se pudo obtener el estado de {machine_id}: {data['error']}"

    # Si la respuesta es un dict con los campos esperados
    return (f"Máquina {data.get('id', machine_id)} ({data.get('name', 'N/A')}):\n"
            f"- Estado: {data.get('status', 'Desconocido')}\n"
            f"- Temperatura: {data.get('temperature', 'N/A')}°C\n"
            f"- Último mantenimiento: {data.get('last_maintenance', 'N/A')}")


# (Opcional) Si quieres darle al agente la capacidad de listar todas las máquinas,
# puedes descomentar esta función y añadirla como herramienta:
#
# def list_all_machines() -> str:
#     """
#     Obtiene el listado de todas las máquinas con su estado actual.
#     """
#     data = get_all_machines()
#     if isinstance(data, dict) and "error" in data:
#         return f"Error al obtener la lista de máquinas: {data['error']}"
#     if not data:
#         return "No hay máquinas registradas."
#     lines = ["Listado de máquinas:"]
#     for m in data:
#         lines.append(f"- {m.get('id', '?')}: {m.get('status', 'desconocido')}")
#     return "\n".join(lines)