# Creates a FAISS vector database from embeddings and text chunks.
# Saves metadata together with each text chunk, including source and page.
# Saves the FAISS database locally.
# Loads the existing FAISS database.
# Searches the FAISS database and returns relevant chunks with metadata.
# Loads PDFs, splits text into chunks, creates embeddings,
# builds the FAISS database, and stores it locally.

import os
import faiss
import numpy as np
import pickle


# Creates a FAISS vector database from embeddings and text chunks.
def create_vector_store(embeddings, documents):

    # Converts embeddings into float32 format required by FAISS.
    embeddings = np.array(embeddings).astype("float32")

    # Normalizes embeddings so Inner Product behaves like
    # cosine similarity.
    faiss.normalize_L2(embeddings)

    # Gets the number of dimensions of the embedding vectors.
    vector_dimension = embeddings.shape[1]

    # Creates an empty FAISS index using Inner Product.
    # With normalized vectors, this is equivalent to cosine similarity.
    index = faiss.IndexFlatIP(vector_dimension)

    # Adds the embedding vectors to the FAISS database.
    index.add(embeddings)

    # Stores the original text chunks and their metadata.
    # Each document contains the text, source file and page number.
    metadata = {
        "documents": documents
    }

    # Returns the FAISS index and associated metadata.
    return index, metadata


# Saves the FAISS database locally.
def save_vector_store(index, metadata):

    # Creates the folder to store the vector database.
    os.makedirs(
        "vector_store",
        exist_ok=True
    )

    # Saves the FAISS index to a file.
    faiss.write_index(
        index,
        "vector_store/faiss.index"
    )

    # Saves the text and document metadata using pickle.
    with open(
        "vector_store/metadata.pkl",
        "wb"
    ) as file:
        pickle.dump(
            metadata,
            file
        )


# Loads the existing FAISS database.
def load_vector_store():

    # Loads the FAISS index from disk.
    index = faiss.read_index(
        "vector_store/faiss.index"
    )

    # Loads the stored metadata from disk.
    with open(
        "vector_store/metadata.pkl",
        "rb"
    ) as file:
        metadata = pickle.load(file)

    # Returns the FAISS index and metadata.
    return index, metadata


# Searches the FAISS database and returns relevant chunks.
def search_vector_store(index, metadata, query_embedding, k=3):

    # Converts the query embedding into FAISS format.
    query_embedding = np.array(
        [query_embedding]
    ).astype("float32")

    # Normalizes the query embedding so Inner Product
    # behaves like cosine similarity.
    faiss.normalize_L2(query_embedding)

    # Searches for the closest vectors in the database.
    distances, indices = index.search(
        query_embedding,
        k
    )

    # Creates a list to store the retrieved documents.
    results = []

    # --- COMPATIBILITY FIX: supports both "documents" and "texts" keys ---
    if "documents" in metadata:
        docs = metadata["documents"]
    elif "texts" in metadata:
        # Convert old format to new format (source unknown)
        docs = [{"text": t, "source": "desconocido", "page": 0} for t in metadata["texts"]]
    else:
        docs = []

    # Loops through the found vector positions and similarity scores.
    for idx, distance in zip(
        indices[0],
        distances[0]
    ):

        # Checks that the index exists in the stored documents.
        if idx >= 0 and idx < len(docs):

            # Gets the document associated with the vector.
            document = docs[idx]

            # Adds the document text, source, page and similarity score.
            results.append(
                {
                    "text": document["text"],
                    "source": document["source"],
                    "page": document["page"],
                    "score": float(distance)
                }
            )

    # Returns the most relevant document chunks with their metadata.
    return results


# Runs this section only when the file is executed directly.
if __name__ == "__main__":

    # Imports functions to load PDFs and split text.
    from src.rag.pdf_loader import load_all_pdfs, split_text

    # Imports the function to create embeddings.
    from src.rag.embeddings import create_embeddings

    # Defines the folder containing the PDF documents.
    documents_folder = "documents"

    # Loads all PDF documents from the folder.
    print("Loading PDFs...")

    raw_docs = load_all_pdfs(
        documents_folder
    )

    # raw_docs is a list of dicts: [{"text": ..., "source": ..., "page": ...}, ...]
    # Extract all texts and combine into a single string.
    all_text = "\n".join([doc["text"] for doc in raw_docs])

    # Split the combined text into chunks (split_text expects a string).
    print("Splitting text...")
    text_chunks = split_text(all_text)

    # Convert each chunk into the required dictionary format (source/page unknown).
    chunks = [
        {"text": chunk, "source": "desconocido", "page": 0}
        for chunk in text_chunks
    ]

    # Displays the number of generated chunks.
    print(
        f"Created {len(chunks)} chunks"
    )

    # Extracts only the text from each chunk for embedding creation.
    print("Creating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(
        texts
    )

    # Creates the FAISS vector database.
    print("Creating FAISS database...")

    index, metadata = create_vector_store(
        embeddings,
        chunks
    )

    # Saves the FAISS database and metadata locally.
    save_vector_store(
        index,
        metadata
    )

    # Confirms that the vector database was created.
    print(
        "Vector store created successfully"
    )