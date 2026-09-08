# src/agent/memory.py
"""
Conversation memory for the agent.
Stores conversation history to provide context for follow-up questions.
"""

class ConversationMemory:
    """Simple conversation memory to store and retrieve chat history."""
    
    def __init__(self, max_history=10):
        """
        Initialize conversation memory.
        
        Args:
            max_history (int): Maximum number of exchanges to keep
        """
        self.history = []
        self.max_history = max_history
    
    def add_exchange(self, user_message, agent_response):
        """
        Add a new exchange to the conversation history.
        
        Args:
            user_message (str): The user's message
            agent_response (str): The agent's response
        """
        self.history.append({
            "user": user_message,
            "agent": agent_response
        })
        
        # Keep only the last max_history exchanges
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_last_user_message(self):
        """
        Get the last user message.
        
        Returns:
            str: The last user message or None if no history
        """
        if self.history:
            return self.history[-1]["user"]
        return None
    
    def get_last_agent_response(self):
        """
        Get the last agent response.
        
        Returns:
            str: The last agent response or None if no history
        """
        if self.history:
            return self.history[-1]["agent"]
        return None
    
    def get_conversation_summary(self):
        """
        Get a summary of the conversation context.
        
        Returns:
            str: Formatted conversation history
        """
        if not self.history:
            return "No previous conversation."
        
        lines = []
        for exchange in self.history:
            lines.append(f"User: {exchange['user']}")
            lines.append(f"Agent: {exchange['agent']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_context_for_question(self, question):
        """
        Provide context for the current question based on conversation history.
        
        Args:
            question (str): The current user question
        
        Returns:
            str: Context to help interpret the question
        """
        if not self.history:
            return ""
        
        # Get last exchange
        last_user = self.get_last_user_message()
        last_agent = self.get_last_agent_response()
        
        context = f"Previous conversation:\nUser: {last_user}\nAgent: {last_agent}\n"
        context += f"\nCurrent question: {question}\n"
        
        return context
    
    def clear(self):
        """Clear all conversation history."""
        self.history = []
    
    def __len__(self):
        """Return the number of exchanges in history."""
        return len(self.history)


# Singleton instance for easy import
memory = ConversationMemory()