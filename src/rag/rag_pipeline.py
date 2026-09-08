
"""
RAG Pipeline - Solo capa de retrieval.
Esta capa se encarga ÚNICAMENTE de recuperar información de los documentos.
La generación de respuestas la maneja el Agent.
"""

from src.rag.embeddings import create_embeddings
from src.rag.vector_store import load_vector_store, search_vector_store


def retrieve_information(question, k=3):
    """
    Recupera los chunks más relevantes de los documentos para una pregunta.
    
    Args:
        question (str): La pregunta del usuario
        k (int): Número de chunks a recuperar (por defecto 3)
    
    Returns:
        list: Lista de textos de los chunks más relevantes
    """
    # Convierte la pregunta en un embedding
    question_embedding = create_embeddings([question])[0]
    
    # Carga el índice FAISS y los metadatos
    index, metadata = load_vector_store()
    
    # Busca los k chunks más relevantes
    results = search_vector_store(
        index,
        metadata,
        question_embedding,
        k=k
    )
    
    # Retorna solo los textos (la generación la hace el Agent)
    return results


def retrieve_information_with_metadata(question, k=3):
    """
    Recupera chunks con metadatos completos (fuente, página, etc.)
    Útil para que el Agent pueda citar fuentes.
    
    Args:
        question (str): La pregunta del usuario
        k (int): Número de chunks a recuperar (por defecto 3)
    
    Returns:
        list: Lista de diccionarios con texto y metadatos
    """
    question_embedding = create_embeddings([question])[0]
    index, metadata = load_vector_store()
    
    # Busca los k chunks más relevantes
    results = search_vector_store(
        index,
        metadata,
        question_embedding,
        k=k
    )
    
    # Retorna los resultados con metadata
    # NOTA: Esto asume que search_vector_store devuelve índices
    # Tendrás que modificar search_vector_store para que devuelva metadata
    
    return results


if __name__ == "__main__":
    # Para pruebas rápidas
    question = input("\nAsk your question: ")
    chunks = retrieve_information(question, k=3)
    
    print("\nRetrieved chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---")
        print(chunk[:200] + "...")  # Muestra solo los primeros 200 caracteres
