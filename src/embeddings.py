# Loads the pre-trained embedding model that converts text into numerical vectors.

# Defines a function that receives text chunks and creates embeddings.

# This block runs only when this file is executed directly.

from sentence_transformers import SentenceTransformer


# Loads the pre-trained embedding model that converts text into numerical vectors.
model = SentenceTransformer("all-MiniLM-L6-v2")


# Defines a function that receives text chunks and creates embeddings.
def create_embeddings(text_chunks):

    # Converts the text chunks into embedding vectors using the loaded model.
    embeddings = model.encode(

        # Sends the list of text chunks to the embedding model.
        text_chunks,

        # Displays a progress bar while creating embeddings.
        show_progress_bar=True
    )

    # Returns the generated embedding vectors.
    return embeddings


# This block runs only when this file is executed directly.
if __name__ == "__main__":

    # Example text chunks for testing the embedding creation.
    sample_chunks = [
        "The motor requires maintenance every 500 hours",
        "The sensor detects temperature changes"
    ]

    # Creates embeddings from the sample text chunks.
    vectors = create_embeddings(sample_chunks)

    # Prints the number of created vectors.
    print("\nNumber of vectors:", len(vectors))

    # Prints the dimension size of the first vector.
    print("Vector size:", len(vectors[0]))


# Loads the pre-trained embedding model that converts text into numerical vectors.

# Defines a function that receives text chunks and creates embeddings.
    # Converts the text chunks into embedding vectors using the loaded model.
        # Sends the list of text chunks to the embedding model.
        # Displays a progress bar while creating embeddings.
    # Returns the generated embedding vectors.

# This block runs only when this file is executed directly.
    # Example text chunks for testing the embedding creation.
    # Creates embeddings from the sample text chunks.
    # Prints the number of created vectors.
    # Prints the dimension size of the first vector.
