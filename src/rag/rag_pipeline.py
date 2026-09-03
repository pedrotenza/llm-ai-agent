# Receives the user's question and retrieves relevant document chunks.
    # Converts the question text into an embedding vector.
    # Loads the FAISS index and document metadata.
    # Searches FAISS and returns the 3 most relevant text chunks.
    # Returns the retrieved chunks to be used as context for the LLM.

# then generates the final answer using the LLM.
    # Creates the Ollama LLM instance using the Qwen2.5 model.
    # Builds the prompt with instructions, context, and user question.
    # Sends the prompt to the LLM and receives the generated answer.
    # Returns only the text content of the LLM response.

# Checks if the script is executed directly.
    # Gets the user's question.
    # Retrieves relevant document chunks.
    # Combines chunks into a single context.
    # Generates the final answer using the LLM.
    # Prints the generated answer.


from src.rag.embeddings import create_embeddings
from src.rag.vector_store import load_vector_store, search_vector_store

from langchain_ollama import ChatOllama


# Receives the user's question and retrieves relevant document chunks.
def retrieve_information(question):

    # Converts the question text into an embedding vector.
    question_embedding = create_embeddings(
        [question]
    )[0]


    # Loads the FAISS index and document metadata.
    index, metadata = load_vector_store()


    # Searches FAISS and returns the 3 most relevant text chunks.
    results = search_vector_store(
        index,
        metadata,
        question_embedding,
        k=3
    )


    # Returns the retrieved chunks to be used as context for the LLM.
    return results


# then generates the final answer using the LLM.
def generate_answer(question, context):

    # Creates the Ollama LLM instance using the Qwen2.5 model.
    llm = ChatOllama(
        model="qwen2.5:0.5b",
        temperature=0,
        num_ctx=128,
        num_predict=100
    )


    # Builds the prompt with instructions, context, and user question.
    prompt = f"""
Du bist ein Assistent für Arbeitssicherheit.

Beantworte die Frage ausschließlich anhand des bereitgestellten Kontexts.

Regeln:
- Antworte auf Deutsch.
- Maximal 2 Sätze.
- Keine Aufzählungen.
- Keine allgemeinen Erklärungen.
- Keine Vermutungen.
- Wiederhole nicht die Frage.
- Wenn die Information nicht im Kontext steht, schreibe:
  "Ich weiß es anhand des Kontexts nicht."

Kontext:
{context}

Frage:
{question}

Antwort:
"""


    # Sends the prompt to the LLM and receives the generated answer.
    response = llm.invoke(prompt)


    # Returns only the text content of the LLM response.
    return response.content


    

# Checks if the script is executed directly.
if __name__ == "__main__":

    # Gets the user's question.
    question = input("\nAsk your question: ")


    # Retrieves relevant document chunks.
    relevant_chunks = retrieve_information(
        question
    )


    # Combines chunks into a single context.
    context = "\n\n".join(
        relevant_chunks
    )


    # Generates the final answer using the LLM.
    answer = generate_answer(
        question,
        context
    )


    # Prints the generated answer.
    print("\n\nAnswer:\n")
    print(answer)


