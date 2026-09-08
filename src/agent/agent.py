# src/agent/agent.py
"""
Main Agent that uses LLM to decide which tools to use.
"""

import re
from langchain_ollama import ChatOllama
from src.config import LLM_MODEL, TEMPERATURE, NUM_CTX, NUM_PREDICT
from src.agent.tools import search_documents, get_machine_info, list_all_machines
from src.agent.prompts import RAG_PROMPT_TEMPLATE, AGENT_DECISION_PROMPT


class SafetyAgent:
    def __init__(self):
        """Initialize the agent with LLM and tools."""
        self.llm = ChatOllama(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            num_ctx=NUM_CTX,
            num_predict=NUM_PREDICT
        )

    def invoke(self, question):
        """
        Process a user question and return a response.
        
        The agent uses LLM to decide which tools to use.
        
        Args:
            question (str): The user's question
        
        Returns:
            str: The agent's response
        """
        # Step 1: Decide which tools to use (using LLM)
        tool_decision = self._decide_tool_with_llm(question)
        
        # Step 2: Execute the appropriate tool
        if tool_decision == "api":
            context = self._use_api_tool(question)
        elif tool_decision == "rag":
            context = self._use_rag_tool(question)
        elif tool_decision == "both":
            context = self._use_both_tools(question)
        else:
            # If decision is unclear, use RAG as default
            context = self._use_rag_tool(question)
        
        # Step 3: Generate the final response
        prompt = RAG_PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )
        
        response = self.llm.invoke(prompt)
        return response.content

    def _decide_tool_with_llm(self, question):
        """
        Use LLM to decide which tool to use.
        
        Returns:
            str: "rag", "api", or "both"
        """
        prompt = AGENT_DECISION_PROMPT.format(question=question)
        
        try:
            response = self.llm.invoke(prompt)
            decision = response.content.strip().lower()
            
            if "api" in decision:
                return "api"
            elif "both" in decision:
                return "both"
            else:
                return "rag"
        except Exception:
            # If LLM fails, use simple rule-based decision
            return self._decide_tool_rule_based(question)

    def _decide_tool_rule_based(self, question):
        """Fallback rule-based tool decision."""
        question_lower = question.lower()
        
        # Check for API keywords
        api_keywords = ['machine', 'máquina', 'status', 'estado', 
                        'temperatura', 'M-', 'temperature']
        
        for keyword in api_keywords:
            if keyword in question_lower:
                return "api"
        
        # Default: use RAG
        return "rag"

    def _use_rag_tool(self, question):
        """Use the RAG tool to search documents."""
        chunks = search_documents(question, k=3)
        
        if not chunks or chunks == ["No information found."]:
            return "No relevant information found in the documents."
        
        return "\n\n".join(chunks)

    def _use_api_tool(self, question):
        """Use the API tool to get machine information."""
        machine_id = self._extract_machine_id(question)
        
        if machine_id:
            try:
                status = get_machine_info(machine_id)
                return self._format_machine_status(status)
            except Exception as e:
                return f"Error getting machine status: {str(e)}"
        
        # If no machine ID, list all machines
        try:
            machines = list_all_machines()
            return self._format_machines_list(machines)
        except Exception as e:
            return f"Error listing machines: {str(e)}"

    def _use_both_tools(self, question):
        """Use both RAG and API tools."""
        rag_context = self._use_rag_tool(question)
        api_context = self._use_api_tool(question)
        
        return f"Documentation:\n{rag_context}\n\nMachine Status:\n{api_context}"

    def _extract_machine_id(self, question):
        """Extract machine ID from question."""
        pattern = r'M-\d{3}'
        match = re.search(pattern, question)
        
        if match:
            return match.group(0)
        
        pattern2 = r'máquina\s+(\d{3})'
        match2 = re.search(pattern2, question.lower())
        
        if match2:
            return f"M-{match2.group(1)}"
        
        return None

    def _format_machine_status(self, status):
        """Format machine status for context."""
        if isinstance(status, dict):
            return "\n".join([f"{k}: {v}" for k, v in status.items()])
        return str(status)

    def _format_machines_list(self, machines):
        """Format machines list for context."""
        if isinstance(machines, list):
            lines = []
            for machine in machines:
                if isinstance(machine, dict):
                    lines.append(f"Machine {machine.get('id', 'Unknown')}: {machine.get('status', 'Unknown')}")
                else:
                    lines.append(str(machine))
            return "\n".join(lines)
        return str(machines)


# Singleton instance for easy import
agent = SafetyAgent()