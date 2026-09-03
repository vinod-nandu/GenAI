# Connecting a LangChain Application to LangSmith for Tracing

To connect a LangChain application to LangSmith for tracing, you need to configure specific environment variables. LangChain automatically detects these variables and sends trace data to LangSmith without requiring extra code changes.

Here is the step-by-step guide to setting up your environment, writing the code, and verifying the traces.

## 1. Set Up a Clean Environment

Open your terminal and run the following commands to create a virtual environment and install the required packages:

```bash
# Create a virtual environment
python -m venv langchain_env

# Activate the environment
# On macOS/Linux:
source langchain_env/bin/activate
# On Windows:
langchain_env\Scripts\activate

# Install the required libraries
pip install langchain-openai python-dotenv
```

## 2. Configure Environment Variables

Create a file named `.env` in your project root directory. This file will securely hold your API keys. LangChain built-in tracing triggers automatically when `LANGCHAIN_TRACING_V2` is set to `true`.

```env
# OpenAI API Key
OPENAI_API_KEY="your-openai-api-key-here"

# LangSmith Configuration
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="your-langsmith-api-key-here"
LANGCHAIN_PROJECT="LangChain-Quickstart" # Optional: Groups your traces
```

## 3. Write the Python Program

Create a file named `app.py` and add the following code. We use `dotenv` to load the environment variables before initializing the OpenAI model.

```python
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
```

## 4. Run the Program and Confirm Tracing

Execute your script in the terminal:

```bash
python app.py
```

### Results

```
(venv) PS C:\Users\Vinod\Dev\langchain-app\venv> python .\app.py
Initializing the OpenAI model...
Sending prompt to model: 'Explain the concept of 'latency' in web applications in one sentence.'
--- Model Output ---
Latency in web applications refers to the delay between a user's action and the application's response.
--------------------
(venv) PS C:\Users\Vinod\Dev\langchain-app\venv>
```




🔎 **Tags:** #GenAI #RAG #LangChain #AIEngineering #OpenAI #DevOps

🙏 **Thanks:** [Thirumurugan R](https://www.linkedin.com/in/thirumurugan-r-85a41b24a/?utm_source=chatgpt.com) & [Manojkumar Vasudevan](https://www.linkedin.com/in/manojkumar-vasudevan-6369b1131/?utm_source=chatgpt.com)

🔗 **LinkedIn** [Article ](https://www.linkedin.com/pulse/langchain-ecosystem-understanding-rag-through-vinodkumar-rajendiran-kgz2c/)

💻 **GitHub:** [GenAI Repository](https://github.com/vinod-nandu/GenAI/tree/main/W2Day3langchain_openai?utm_source=chatgpt.com)

🚀 Learn • Build • Experiment • Share
