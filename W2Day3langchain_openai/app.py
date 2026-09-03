import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables from the .env file
load_dotenv()

def main():
    print("Initializing the OpenAI model...")
    # Initialize the ChatOpenAI model (defaults to gpt-4o)
    model = ChatOpenAI(temperature=0.7)

    # Define the input prompt
    user_input = "Explain the concept of 'latency' in web applications in one sentence."
    messages = [HumanMessage(content=user_input)]

    print(f"Sending prompt to model: '{user_input}'")
    
    # Run the model (this action triggers the LangSmith trace)
    response = model.invoke(messages)

    # Print the output
    print("\n--- Model Output ---")
    print(response.content)
    print("--------------------")

if __name__ == "__main__":
    main()
