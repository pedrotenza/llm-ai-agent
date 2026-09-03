from rag.rag_pipeline import retrieve_information


def search_documents(question: str) -> str:
    """
    Busca información relevante en los documentos.
    """

    results = retrieve_information(question)

    if not results:
        return "No se encontró información relevante."

    return "\n\n".join(results)