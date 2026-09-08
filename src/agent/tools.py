# src/agent/tools.py
"""
Tools that the agent can use to interact with the system.
These tools abstract away the complexity of the underlying systems (RAG, API, etc.).
"""

from src.rag.rag_pipeline import retrieve_information
from src.api.services import get_machine_status, get_all_machines


def search_documents(question, k=3):
    """
    Search for relevant information in the documents.

    Args:
        question (str): The user's question to search for
        k (int): Number of chunks to retrieve (default: 3)

    Returns:
        list: List of text chunks relevant to the question

    Example:
        >>> search_documents("How often should the machine be maintained?")
        ['The machine should be maintained every 500 hours...', ...]
    """
    results = retrieve_information(question, k=k)
    
    if not results:
        return ["No information found."]
    
    return results


def get_machine_info(machine_id):
    """
    Get current status and information about a specific machine.

    Args:
        machine_id (str): The machine identifier

    Returns:
        dict: Machine status information

    Example:
        >>> get_machine_info("M-102")
        {'id': 'M-102', 'status': 'running', 'temperature': 84}
    """
    return get_machine_status(machine_id)


def list_all_machines():
    """
    Get information about all machines.

    Returns:
        list: List of all machines with their status

    Example:
        >>> list_all_machines()
        [{'id': 'M-101', 'status': 'running'}, {'id': 'M-102', 'status': 'idle'}]
    """
    return get_all_machines()