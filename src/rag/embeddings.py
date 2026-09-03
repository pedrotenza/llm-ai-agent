from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(text_chunks):
    """
    Creates normalized embedding vectors for a list of text chunks.
    """
    return model.encode(
        text_chunks,
        show_progress_bar=True,
        normalize_embeddings=True
    )


if __name__ == "__main__":
    sample_chunks = [
        "The motor requires maintenance every 500 hours",
        "The sensor detects temperature changes"
    ]

    vectors = create_embeddings(sample_chunks)

    print("\nNumber of vectors:", len(vectors))
    print("Vector size:", len(vectors[0]))