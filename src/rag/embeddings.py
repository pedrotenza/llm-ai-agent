# Imports the SentenceTransformer library for creating text embeddings.
# Defines the name of the embedding model.
# Loads the SentenceTransformer embedding model.
# Creates normalized embedding vectors for a list of text chunks.
# Encodes the text chunks into embedding vectors.
# Shows a progress bar while creating the embeddings.
# Normalizes the embedding vectors.
# Checks if the script is executed directly.
# Creates sample text chunks for testing the embedding model.
# Generates embedding vectors for the sample chunks.
# Prints the number of generated vectors.
# Prints the size of each embedding vector.


# Imports the SentenceTransformer library for creating text embeddings.
from sentence_transformers import SentenceTransformer


# Defines the name of the embedding model.
MODEL_NAME = "all-MiniLM-L6-v2"


# Loads the SentenceTransformer embedding model.
model = SentenceTransformer(MODEL_NAME)


# Creates normalized embedding vectors for a list of text chunks.
def create_embeddings(text_chunks):
    """
    Creates normalized embedding vectors for a list of text chunks.
    """
    return model.encode(
        text_chunks,
        show_progress_bar=True,
        normalize_embeddings=True
    )


# Checks if the script is executed directly.
# Creates sample text chunks for testing the embedding model.
# Generates embedding vectors for the sample chunks.
# Prints the number of generated vectors.
# Prints the size of each embedding vector.

if __name__ == "__main__":

    # Creates sample text chunks for testing the embedding model.
    sample_chunks = [
        "The motor requires maintenance every 500 hours",
        "The sensor detects temperature changes"
    ]

    # Generates embedding vectors for the sample chunks.
    vectors = create_embeddings(sample_chunks)

    # Prints the number of generated vectors.
    print("\nNumber of vectors:", len(vectors))

    # Prints the size of each embedding vector.
    print("Vector size:", len(vectors[0]))