# src/main.py
"""
Main entry point for the Safety Assistant Agent.
"""

from src.agent.agent import invoke_agent


def main():
    """Main interaction loop."""
    print("🤖 Occupational Safety Assistant (Agent + RAG + API)")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("User: ").strip()

        if question.lower() in ["exit", "quit", "salir"]:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            response = invoke_agent(question)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()