# src/main.py

# Runs the main interaction loop of the Safety Assistant.

# Imports the Agent function used to process user questions.
# Allows the user to ask multiple questions in the same execution.
# Allows the user to exit the application with specific commands.
# Handles errors that may occur while processing a question.
# Runs the main function when the file is executed directly.


# Imports the invoke_agent function from the Agent module.
from src.agent.agent import invoke_agent


# Defines the main function that controls the user interaction.
def main():

    # Prints the title of the Safety Assistant.
    print("🤖 Occupational Safety Assistant (Agent + RAG + API)")

    # Prints the commands that can be used to exit the application.
    print("Type 'exit' to quit.\n")

    # Creates an infinite loop to allow multiple user questions.
    while True:

        # Asks the user to enter a question and removes extra spaces.
        question = input("User: ").strip()

        # Checks if the user wants to exit the application.
        if question.lower() in ["exit", "quit", "salir"]:
            # Prints a goodbye message.
            print("Goodbye!")

            # Stops the interaction loop.
            break

        # Checks if the user entered an empty question.
        if not question:
            # Starts the next iteration of the loop.
            continue

        # Tries to process the user's question.
        try:
            # Sends the question to the Agent.
            response = invoke_agent(question)

            # Prints the Agent response.
            print(f"\nAgent: {response}\n")

        # Handles errors that occur while processing the question.
        except Exception as e:
            # Prints the error message.
            print(f"\nError: {str(e)}\n")


# Checks if this file is being executed directly.
if __name__ == "__main__":

    # Starts the main interaction loop.
    main()

