# src/agent/agent.py


# Creates a multilingual semantic router to classify user questions.
# Uses the LLM as a fallback when the semantic router is not confident.
# Decides whether to use RAG, API or no tool for each question.
# Supports multi-intent detection: multiple tools can be executed at once.
# Executes the selected tool(s) and generates the final answer with the LLM.
# Extracts machine IDs from user questions.
# Runs the Agent when the file is executed directly.


import re
import numpy as np
from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer

from src.agent.tools import search_documents, get_machine_api_status
from src.agent.prompts import SYSTEM_PROMPT
from src.agent.memory import memory
from src.config import (
    LLM_MODEL,
    TEMPERATURE,
    NUM_CTX,
    NUM_PREDICT,
    ROUTER_THRESHOLD,
    ROUTER_NONE_THRESHOLD,
    EMBEDDING_MODEL,
)


llm = ChatOllama(
    model=LLM_MODEL,
    temperature=TEMPERATURE,
    num_ctx=NUM_CTX,
    num_predict=NUM_PREDICT
)


# Creates the embedding model used by the multilingual semantic router.
_embedder = SentenceTransformer(EMBEDDING_MODEL)

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

# Defines keywords that indicate the question refers to a manual or document.
_MANUAL_KEYWORDS = [
    "manual", "handbuch", "manuale", "manuel",
    "procedure", "procedimiento", "procedura", "procédure",
    "normativa", "regulation", "reglamento", "regolamento",
    "safety manual", "handbook",
]


# Defines a function called _semantic_decisions that receives one question.
def _semantic_decisions(question: str) -> list[str]:
    """
    Returns a list of labels (API, RAG, NONE) whose similarity
    exceeds the threshold. Can return multiple labels.
    Works in any language supported by the model.
    """

    # Converts the user question into a normalized embedding.
    q_vec = _embedder.encode([question], normalize_embeddings=True)[0]

    # Calculates the similarity between the question and all router examples.
    sims = _ROUTER_VECTORS @ q_vec

    # Best score per label
    label_scores = {}
    for label, score in zip(_ROUTER_VECTOR_LABELS, sims):
        if label not in label_scores or score > label_scores[label]:
            label_scores[label] = float(score)

    # Prints all label scores sorted from highest to lowest.
    print("[DEBUG] Semantic router scores:")
    for label, score in sorted(label_scores.items(), key=lambda x: -x[1]):
        print(f"        {label:<6} = {score:.3f}")

    # Applies a different threshold for NONE to avoid false positives.
    selected = []
    for label, score in label_scores.items():
        if label == "NONE":
            if score >= ROUTER_NONE_THRESHOLD:
                selected.append(label)
        else:
            if score >= ROUTER_THRESHOLD:
                selected.append(label)

    # Prints the selected labels after applying the thresholds.
    print(f"[DEBUG] Selected labels: {selected}")

    # Returns the list of selected labels (may be empty).
    return selected


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
    Decides which tool should be used (single-tool mode).

    1. Multilingual semantic router.
    2. LLM fallback if the semantic router is not confident.

    Returns:
        RAG  -> information from internal documents
        API  -> current information about a machine
        NONE -> no tool is required
    """

    # Calls the semantic router to classify the question (multi-intent).
    semantic = _semantic_decisions(question)

    # Checks if the semantic router returned at least one confident decision.
    if semantic:
        # Picks the first label as the primary decision (single-tool mode).
        decision = semantic[0]

        # Prints the decision made by the semantic router.
        print(f"[DEBUG] Tool decision by semantic router: {decision}")

        # Returns the semantic router decision.
        return decision

    # Calls the LLM router when the semantic router is not confident.
    decision = _llm_decision(question)

    # Prints the decision made by the LLM.
    print(f"[DEBUG] Tool decision by LLM: {decision}")

    # Returns the LLM decision.
    return decision


# Defines a function called invoke_agent that receives one question.
def invoke_agent(question: str) -> str:
    """
    Main Agent logic with multi-intent support.

    1. The router decides which labels (RAG, API, NONE) apply.
    2. All selected tools are executed.
    3. The LLM generates the final answer.
    """

    # Retrieves the conversation context relevant to the question.
    memory_context = memory.get_context_for_question(question)

    # Multi-intent detection using the semantic router.
    decisions = _semantic_decisions(question)

    # Fallback to LLM if nothing selected by the semantic router.
    if not decisions:
        print("[DEBUG] Semantic router: low confidence, falling back to LLM.")
        decisions = [_llm_decision(question)]

    # --- Multi-tool rule: manual keyword + machine ID -> RAG + API ---

    # Checks if the question mentions a manual or document.
    mentions_manual = any(kw in question.lower() for kw in _MANUAL_KEYWORDS)

    # Checks if the question mentions a machine ID.
    mentions_machine = extract_machine_id(question) is not None

    # If both are present, ensure both RAG and API are executed.
    if mentions_manual and mentions_machine:
        if "RAG" not in decisions:
            decisions.append("RAG")
        if "API" not in decisions:
            decisions.append("API")
        print("[DEBUG] Multi-tool rule triggered: RAG + API added to decisions.")

    # Prints the final list of decisions.
    print(f"[DEBUG] Final decisions: {decisions}")

    # Creates an empty list to store tool results.
    observations = []

    # Executes the RAG tool if selected.
    if "RAG" in decisions:
        # Prints that the RAG tool is being executed.
        print("[DEBUG] Executing RAG tool...")

        # Searches the internal documents using the user's question.
        observations.append(search_documents(question))

    # Executes the API tool if selected.
    if "API" in decisions:
        # Prints that the API tool is being executed.
        print("[DEBUG] Executing API tool...")

        # Extracts the machine ID from the question or from memory.
        machine_id = extract_machine_id(question) or extract_machine_id(memory_context)

        # Checks if a machine ID was found.
        if machine_id:
            # Gets the current machine information from the API.
            observations.append(get_machine_api_status(machine_id))
        else:
            # Adds an error message when no machine ID is found.
            observations.append("No pude identificar el ID de la máquina en la pregunta.")

    # Checks if no tool is required.
    if "NONE" in decisions and not observations:
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

    # Extracts the final answer.
    answer = response.content.strip()

    # Stores the exchange in memory.
    memory.add_exchange(question, answer)

    # Returns the final answer.
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