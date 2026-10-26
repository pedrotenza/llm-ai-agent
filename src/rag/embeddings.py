
# Defines the name of the sentence-transformer model used to create embeddings.
# Initializes the sentence-transformer model using the selected model name.
# Defines a function that creates normalized embedding vectors from text chunks.
# Checks if this file is being executed directly.

from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL


# Defines the name of the sentence-transformer model used to create embeddings.
MODEL_NAME = "all-MiniLM-L6-v2"


# Initializes the sentence-transformer model using the selected model name.
model = SentenceTransformer(MODEL_NAME)


# Defines a function that creates normalized embedding vectors from text chunks.
def create_embeddings(text_chunks):
    """
    Creates normalized embedding vectors for a list of text chunks.
    """

    # Converts the text chunks into embedding vectors.
    # Displays a progress bar while the embeddings are being generated.
    # Normalizes the resulting embedding vectors.
    return model.encode(
        text_chunks,
        show_progress_bar=True,
        normalize_embeddings=True
    )


# Checks if this file is being executed directly.
if __name__ == "__main__":

    # Defines sample text chunks to demonstrate the embedding process.
    sample_chunks = [
        "The motor requires maintenance every 500 hours",
        "The sensor detects temperature changes"
    ]

    # Creates embedding vectors for the sample text chunks.
    vectors = create_embeddings(sample_chunks)

    # Displays the number of generated embedding vectors.
    print("\nNumber of vectors:", len(vectors))

    # Displays the size of each embedding vector.
    print("Vector size:", len(vectors[0]))