# src/agent/agent.py


# Creates a multilingual semantic router to classify user questions.
# Uses the LLM as a fallback when the semantic router is not confident.
# Decides whether to use RAG, API or no tool for each question.
# Executes the selected tool and generates the final answer with the LLM.
# Extracts machine IDs from user questions.
# Runs the Agent when the file is executed directly.


import re
import numpy as np
from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer

from src.agent.tools import search_documents, get_machine_api_status
from src.agent.prompts import SYSTEM_PROMPT
from src.agent.memory import memory
from src.config import LLM_MODEL, TEMPERATURE, NUM_CTX


llm = ChatOllama(
    model=LLM_MODEL,
    temperature=TEMPERATURE,
    num_ctx=NUM_CTX
)


# Creates a multilingual semantic router.
_embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Creates example questions for each possible tool decision.
_ROUTER_EXAMPLES = {
    "API": [
        # Spanish
        "¿Cuál es el estado actual de M-102?",
        "¿Cuál es la temperatura de M-102?",
        "¿Cuándo fue el último mantenimiento de M-102?",
        "¿Está funcionando la máquina M-102?",
        # English
        "What is the current status of M-102?",
        "What is the current temperature of M-102?",
        "When was M-102 last maintained?",
        "Is machine M-102 running?",
        # Italiano
        "Qual è lo stato attuale di M-102?",
        "Qual è la temperatura di M-102?",
        "Quando è stata l'ultima manutenzione di M-102?",
        # Deutsch
        "Wie ist der aktuelle Status von M-102?",
        "Wie ist die aktuelle Temperatur von M-102?",
        # Français
        "Quel est l'état actuel de M-102?",
        "Quelle est la température actuelle de M-102?",
    ],
    "RAG": [
        # Spanish
        "¿Qué dice el manual sobre el mantenimiento preventivo?",
        "¿Qué dice el procedimiento sobre seguridad?",
        "¿Qué dice la normativa sobre el equipo de protección?",
        # English
        "What does the safety manual say about preventive maintenance?",
        "What does the procedure say about machine safety?",
        "What does the regulation say about personal protective equipment?",
        # Italiano
        "Cosa dice il manuale sulla manutenzione preventiva?",
        "Cosa dice la procedura sulla sicurezza?",
        # Deutsch
        "Was sagt das Handbuch über vorbeugende Wartung?",
        # Français
        "Que dit le manuel sur la maintenance préventive?",
    ],
    "NONE": [
        "What is 2 + 2?",
        "¿Cuánto es 2 + 2?",
        "Quanto fa 2 + 2?",
        "¿Qué hora es?",
        "What time is it?",
        "Che ore sono?",
    ],
}

# Creates a list with all available router labels.
_ROUTER_LABELS = list(_ROUTER_EXAMPLES.keys())

# Creates a list with all example questions.
_ROUTER_TEXTS = [t for label in _ROUTER_LABELS for t in _ROUTER_EXAMPLES[label]]

# Converts all example questions into normalized embeddings.
_ROUTER_VECTORS = _embedder.encode(_ROUTER_TEXTS, normalize_embeddings=True)

# Creates a label for each example question.
_ROUTER_VECTOR_LABELS = [
    label for label in _ROUTER_LABELS for _ in _ROUTER_EXAMPLES[label]
]

# Defines the minimum similarity score required by the semantic router.
_ROUTER_THRESHOLD = 0.45


# Defines a function called _semantic_decision that receives one question.
def _semantic_decision(question: str) -> str | None:
    """
    Returns API, RAG, NONE or None if the similarity is low.
    Works in any language supported by the model.
    """

    # Converts the user question into a normalized embedding.
    q_vec = _embedder.encode([question], normalize_embeddings=True)[0]

    # Calculates the similarity between the question and all router examples.
    sims = _ROUTER_VECTORS @ q_vec

    # Finds the position of the most similar example.
    best_idx = int(np.argmax(sims))

    # Gets the similarity score of the best example.
    best_score = float(sims[best_idx])

    # Gets the label of the most similar example.
    best_label = _ROUTER_VECTOR_LABELS[best_idx]

    # Prints the semantic router decision and similarity score.
    print(f"[DEBUG] Semantic router: {best_label} (score={best_score:.3f})")

    # Checks if the similarity score is below the confidence threshold.
    if best_score < _ROUTER_THRESHOLD:
        # Prints that the semantic router is not confident enough.
        print("[DEBUG] Semantic router: low confidence, falling back to LLM.")

        # Returns None so the LLM can make the decision.
        return None

    # Returns the decision made by the semantic router.
    return best_label


# Defines a function called _llm_decision that receives one question.
def _llm_decision(question: str) -> str:
    """
    Fallback: LLM router if the semantic router is not confident.
    """

    # Creates the prompt used to classify the user's question.
    router_prompt = f"""
You are the decision maker of an occupational safety assistant.

You have three possible choices:

RAG
Use RAG when the answer requires information from internal
documents, manuals, procedures, regulations or safety documentation.

API
Use API when the answer requires current information about a machine,
such as status, temperature or maintenance information.

NONE
Use NONE when no tool is necessary.

Rules:

- Choose exactly ONE option.
- Return ONLY one of these words:
  RAG
  API
  NONE

Examples:

Question: What is the current status of M-102?
Decision: API

Question: What is the current temperature of M-102?
Decision: API

Question: When was M-102 last maintained?
Decision: API

Question: What does the safety manual say about preventive maintenance?
Decision: RAG

Question: What does the procedure say about machine safety?
Decision: RAG

Question: What does the regulation say about personal protective equipment?
Decision: RAG

Question: What is 2 + 2?
Decision: NONE

Do not explain your decision.
Do not write anything else.

Now classify the user's question.

User question:
{question}

Decision:
"""

    # Sends the router prompt to the LLM.
    response = llm.invoke(router_prompt)

    # Extracts and normalizes the LLM decision.
    decision = response.content.strip().upper()

    # Removes the "DECISION:" text if the LLM includes it.
    decision = decision.replace("DECISION:", "").strip()

    # Prints the decision made by the LLM.
    print(f"[DEBUG] LLM router: {decision}")

    # Checks if the decision is one of the valid options.
    if decision in ["RAG", "API", "NONE"]:
        # Returns the valid decision.
        return decision

    # Loops through the valid options to find one inside the response.
    for option in ["API", "RAG", "NONE"]:
        # Checks if the current option appears in the LLM response.
        if option in decision:
            # Returns the detected option.
            return option

    # Prints a message when the LLM returns an invalid decision.
    print("[DEBUG] Invalid decision. Using NONE.")

    # Returns NONE when no valid decision is found.
    return "NONE"


# Defines a function called decide_tool that receives one question.
def decide_tool(question: str) -> str:
    """
    Decides which tool should be used.

    1. Multilingual semantic router.
    2. LLM fallback if the semantic router is not confident.

    Returns:
        RAG  -> information from internal documents
        API  -> current information about a machine
        NONE -> no tool is required
    """

    # Calls the semantic router to classify the question.
    semantic = _semantic_decision(question)

    # Checks if the semantic router returned a confident decision.
    if semantic is not None:
        # Prints the decision made by the semantic router.
        print(f"[DEBUG] Tool decision by semantic router: {semantic}")

        # Returns the semantic router decision.
        return semantic

    # Calls the LLM router when the semantic router is not confident.
    decision = _llm_decision(question)

    # Prints the decision made by the LLM.
    print(f"[DEBUG] Tool decision by LLM: {decision}")

    # Returns the LLM decision.
    return decision


# Defines a function called invoke_agent that receives one question.
def invoke_agent(question: str) -> str:
    """
    Main Agent logic.

    1. The router decides RAG, API or NONE.
    2. The selected tool is executed.
    3. The LLM generates the final answer.
    """

    memory_context = memory.get_context_for_question(question)

    # Calls the router to decide which tool should be used.
    decision = decide_tool(question)

    # Creates an empty list to store tool results.
    observations = []

    # Checks if the selected tool is RAG.
    if decision == "RAG":
        # Prints that the RAG tool is being executed.
        print("[DEBUG] Executing RAG tool...")

        # Searches the internal documents using the user's question.
        result = search_documents(question)

        # Adds the search result to the observations list.
        observations.append(result)

    # Checks if the selected tool is API.
    elif decision == "API":
        # Prints that the API tool is being executed.
        print("[DEBUG] Executing API tool...")

        # Extracts the machine ID from the user's question.
        machine_id = extract_machine_id(question)

        if not machine_id:
            machine_id = extract_machine_id(memory_context)

        # Checks if a machine ID was found.
        if not machine_id:
            # Returns an error message when no machine ID is found.
            return "No pude identificar el ID de la máquina en la pregunta."

        # Gets the current machine information from the API.
        result = get_machine_api_status(machine_id)

        # Adds the API result to the observations list.
        observations.append(result)

    # Checks if no tool is required.
    elif decision == "NONE":
        # Prints that no tool is required.
        print("[DEBUG] No tool required.")

    # Combines all tool results into one context string.
    context = "\n\n".join(observations)

    # Creates the final prompt used to generate the answer.
    final_prompt = f"""
{SYSTEM_PROMPT}

You are now answering the user's question.

Previous conversation:
{memory_context}

If tool information is provided below, use it as the primary source.
Do not invent information.
Do not claim that you checked a tool if no tool was used.

Tool information:
{context}

User question:
{question}

Provide the final answer directly to the user.
"""

    # Sends the final prompt to the LLM.
    response = llm.invoke(final_prompt)

    answer = response.content.strip()

    memory.add_exchange(question, answer)

    return answer


# Defines a function called extract_machine_id that receives one question.
def extract_machine_id(question: str) -> str | None:
    """
    Extracts a machine ID such as M-101 or M-102 from the question.
    """

    # Searches for a machine ID with the format M-number.
    match = re.search(r"\bM-\d+\b", question.upper())

    # Checks if a machine ID was found.
    if match:
        # Returns the machine ID found in the question.
        return match.group(0)

    # Returns None when no machine ID is found.
    return None


# Checks if this file is being executed directly.
if __name__ == "__main__":

    # Asks the user to enter a question.
    question = input("\nAsk your question: ")

    # Sends the question to the Agent.
    answer = invoke_agent(question)

    # Prints the answer heading.
    print("\n\nAnswer:\n")

    # Prints the final Agent answer.
    print(answer)