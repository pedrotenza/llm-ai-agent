
# Creates a FAISS vector database from embeddings and text chunks.
# Saves the FAISS database locally.
# Loads the existing FAISS database.
# Searches the FAISS database and returns relevant chunks.
# Loads PDFs, splits text into chunks, creates embeddings,
# builds the FAISS database, and stores it locally.

import os
import faiss
import numpy as np
import pickle


# Creates a FAISS vector database from embeddings and text chunks.
def create_vector_store(embeddings, text_chunks):

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

    # Stores the original text chunks as metadata.
    metadata = {
        "texts": text_chunks
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

    # Saves the text metadata using pickle.
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

    # Creates a list to store the retrieved text chunks.
    results = []

    # Loops through the found vector positions.
    for idx in indices[0]:

        # Checks that the index exists in the stored texts.
        if idx >= 0 and idx < len(metadata["texts"]):

            # Adds the corresponding text chunk to the results.
            results.append(
                metadata["texts"][idx]
            )

    # Returns the most relevant document chunks.
    return results


# Runs this section only when the file is executed directly.
if __name__ == "__main__":

    # Imports functions to load PDFs and split text.
    from src.pdf_loader import load_all_pdfs, split_text

    # Imports the function to create embeddings.
    from src.embeddings import create_embeddings

    # Defines the folder containing the PDF documents.
    documents_folder = "documents"

    # Loads all PDF documents from the folder.
    print("Loading PDFs...")

    text = load_all_pdfs(
        documents_folder
    )

    # Splits the document text into smaller chunks.
    print("Splitting text...")

    chunks = split_text(
        text
    )

    # Displays the number of generated chunks.
    print(
        f"Created {len(chunks)} chunks"
    )

    # Converts text chunks into embedding vectors.
    print("Creating embeddings...")

    embeddings = create_embeddings(
        chunks
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

