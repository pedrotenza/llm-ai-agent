# src/agent/agent.py
import re
from langchain_ollama import ChatOllama
from src.agent.tools import search_documents, get_machine_api_status
from src.agent.prompts import SYSTEM_PROMPT
from src.config import LLM_MODEL, TEMPERATURE

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=TEMPERATURE,
    num_ctx=4096
)

TOOL_MAP = {
    "search_documents": search_documents,
    "get_machine_api_status": get_machine_api_status,
}

def invoke_agent(question: str, max_iterations: int = 5) -> str:
    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", question)
    ]
    
    for _ in range(max_iterations):
        response = llm.invoke(messages)
        content = response.content

        # 🆕 Línea añadida para depuración: muestra el contenido completo generado por el LLM
        print(f"[DEBUG] LLM response:\n{content}\n{'-'*50}")

        # Look for Action and Action Input
        action_match = re.search(r"Action:\s*(\w+)", content)
        action_input_match = re.search(r"Action Input:\s*(.+)", content)
        
        if action_match and action_input_match:
            tool_name = action_match.group(1).strip()
            tool_input = action_input_match.group(1).strip().strip('"')
            
            if tool_name in TOOL_MAP:
                observation = TOOL_MAP[tool_name](tool_input)
                messages.append(("assistant", content))
                messages.append(("user", f"Observation: {observation}"))
                continue  # Call the LLM again with the observation
        
        # If there's no Action, look for Final Answer
        final_match = re.search(r"Final Answer:\s*(.+)", content, re.DOTALL)
        if final_match:
            return final_match.group(1).strip()
        else:
            return content.strip()
    
    return "Sorry, I couldn't process your request within the maximum number of iterations."