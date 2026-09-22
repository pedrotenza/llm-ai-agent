"""
RAG Pipeline - Pure retrieval layer.
This layer is responsible ONLY for retrieving information from documents.
Response generation is handled by the Agent.
"""

from src.config import RAG_MIN_SCORE, RAG_TOP_K
from src.rag.embeddings import create_embeddings
from src.rag.vector_store import load_vector_store, search_vector_store


def retrieve_information(question, k=RAG_TOP_K, min_score=RAG_MIN_SCORE):
    """
    Retrieves the most relevant document chunks for a question.
    
    Args:
        question (str): The user's question
        k (int): Number of chunks to retrieve (default RAG_TOP_K)
        min_score (float): Minimum similarity score to keep a chunk (default RAG_MIN_SCORE)
    
    Returns:
        list: List of dictionaries with text and metadata
    """
    # Convert the question into an embedding
    question_embedding = create_embeddings([question])[0]
    
    # Load the FAISS index and metadata
    index, metadata = load_vector_store()
    
    # Search for the k most relevant chunks
    results = search_vector_store(
        index,
        metadata,
        question_embedding,
        k=k
    )
    
    # Filter out chunks with a score below the minimum threshold
    results = [r for r in results if r["score"] >= min_score]
    
    # Return results with metadata
    return results


def retrieve_information_with_metadata(question, k=RAG_TOP_K, min_score=RAG_MIN_SCORE):
    """
    Retrieves chunks with full metadata (source, page, etc.).
    Useful for the Agent to cite sources.
    
    Args:
        question (str): The user's question
        k (int): Number of chunks to retrieve (default RAG_TOP_K)
        min_score (float): Minimum similarity score to keep a chunk (default RAG_MIN_SCORE)
    
    Returns:
        list: List of dictionaries with text and metadata
    """
    question_embedding = create_embeddings([question])[0]
    index, metadata = load_vector_store()
    
    results = search_vector_store(
        index,
        metadata,
        question_embedding,
        k=k
    )
    
    # Filter out chunks with a score below the minimum threshold
    results = [r for r in results if r["score"] >= min_score]
    
    return results


if __name__ == "__main__":
    # Quick test
    question = input("\nAsk your question: ")
    chunks = retrieve_information(question, k=RAG_TOP_K)
    
    print("\nRetrieved chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Text: {chunk['text'][:200]}...")   # First 200 characters
        print(f"Source: {chunk.get('source', 'unknown')}")
        print(f"Page: {chunk.get('page', 'N/A')}")
        print(f"Score: {chunk.get('score', 0):.4f}")