"""
=====================================================================
 BASIC GENAI APPLICATION USING LANGCHAIN — BEGINNER WALKTHROUGH
=====================================================================
This single file teaches you LangChain step by step by BUILDING the
same app in increasing layers of capability:

  LAYER 1: Call an LLM directly (no LangChain magic yet)
  LAYER 2: Use a Prompt Template (reusable, fill-in-the-blank prompts)
  LAYER 3: Use an Output Parser (clean up the model's response)
  LAYER 4: Chain them together using LCEL (LangChain Expression Language)
  LAYER 5: Add Memory (so it remembers the conversation)
  LAYER 6: Wrap it all into an interactive chatbot loop

Run each layer's function separately (see the bottom of the file)
to see how the app grows more powerful at each step.
=====================================================================
"""

import os
from dotenv import load_dotenv

# load_dotenv() reads your .env file and loads OPENAI_API_KEY
# into the environment, so LangChain can find it automatically.
load_dotenv()


# =====================================================================
# LAYER 1: Talk to an LLM directly
# =====================================================================
# ChatOpenAI is a "wrapper" class. It doesn't contain the AI model
# itself — it just knows HOW to send requests to OpenAI's API and
# parse the responses into a common LangChain format.
def layer1_basic_llm_call():
    from langchain_openai import ChatOpenAI

    # temperature=0   -> deterministic, focused answers (good for facts/code)
    # temperature=0.7 -> more creative, varied answers (good for writing)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # .invoke() sends a single message and waits for the full response.
    # Passing a plain string is treated as a "human" message.
    response = llm.invoke("Explain what an API is in one sentence.")

    # The response is a "message object", not plain text.
    # response.content holds the actual text reply.
    print("LAYER 1 OUTPUT:\n", response.content)


# =====================================================================
# LAYER 2: Use a Prompt Template
# =====================================================================
# Hardcoding prompts (like above) doesn't scale. In real apps, you want
# a TEMPLATE where certain parts change based on user input.
# ChatPromptTemplate lets you define placeholders like {topic}.
def layer2_prompt_template():
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # from_messages() builds a structured prompt with roles:
    #   "system" -> sets the AI's behavior/persona (not shown to user)
    #   "human"  -> the actual user's message, with a {placeholder}
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly teacher who explains things simply."),
        ("human", "Explain {topic} in 2 lines for a complete beginner.")
    ])

    # .invoke() on a PROMPT fills in the placeholders and returns
    # a formatted prompt (list of messages), NOT the AI's answer yet.
    formatted_prompt = prompt.invoke({"topic": "machine learning"})

    # Now we manually pass that formatted prompt to the LLM.
    response = llm.invoke(formatted_prompt)

    print("LAYER 2 OUTPUT:\n", response.content)


# =====================================================================
# LAYER 3: Output Parsers
# =====================================================================
# response.content works fine, but for bigger apps you often want the
# result auto-converted into plain strings, lists, or structured JSON.
# StrOutputParser simply extracts .content for you automatically.
def layer3_output_parser():
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly teacher."),
        ("human", "Explain {topic} in 2 lines.")
    ])
    parser = StrOutputParser()  # just extracts plain text from the AI response

    formatted_prompt = prompt.invoke({"topic": "neural networks"})
    raw_response = llm.invoke(formatted_prompt)
    clean_text = parser.invoke(raw_response)  # same as raw_response.content

    print("LAYER 3 OUTPUT:\n", clean_text)


# =====================================================================
# LAYER 4: Chains using LCEL (the "|" pipe operator)
# =====================================================================
# Manually calling prompt -> llm -> parser step by step (like above)
# gets repetitive. LangChain lets you CHAIN them with the "|" operator,
# similar to Unix pipes. Data flows left to right automatically.
def layer4_lcel_chain():
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly teacher."),
        ("human", "Explain {topic} in 2 lines.")
    ])
    parser = StrOutputParser()

    # THIS is the core LangChain idiom you'll see everywhere:
    # chain = prompt | llm | parser
    # It means: "take the input, format it into a prompt,
    #            send it to the llm, then parse the output"
    chain = prompt | llm | parser

    # Now a 3-step process becomes ONE call:
    result = chain.invoke({"topic": "vector databases"})

    print("LAYER 4 OUTPUT:\n", result)


# =====================================================================
# LAYER 5: Adding Memory (conversation history)
# =====================================================================
# So far, every .invoke() call is STATELESS — the model has no idea
# what you asked before. To build a real chatbot, we need to track
# conversation history and feed it back in each time.
def layer5_chain_with_memory():
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.messages import HumanMessage, AIMessage

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # MessagesPlaceholder reserves a spot in the prompt where we'll
    # inject the ENTIRE chat history (a list of past messages).
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Keep answers concise."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    parser = StrOutputParser()
    chain = prompt | llm | parser

    # chat_history is just a plain Python list we manage ourselves.
    # HumanMessage = something the user said
    # AIMessage    = something the AI replied
    chat_history = []

    def ask(user_input: str):
        response = chain.invoke({
            "input": user_input,
            "history": chat_history
        })
        # After getting a reply, we APPEND both messages to history
        # so the next call remembers this exchange.
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        return response

    print("LAYER 5 OUTPUT:")
    print("Bot:", ask("My name is Arjun."))
    print("Bot:", ask("What's my name?"))  # it should now remember!


# =====================================================================
# LAYER 6: Putting it all together — an interactive chatbot loop
# =====================================================================
# This is the "final app" — combining prompt + chain + memory into
# a simple command-line chatbot you can actually talk to.
def run_chatbot():
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.messages import HumanMessage, AIMessage

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, friendly assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm | StrOutputParser()
    chat_history = []

    print("=" * 50)
    print(" Simple LangChain Chatbot — type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break

        # Run the chain with current input + accumulated history
        response = chain.invoke({
            "input": user_input,
            "history": chat_history
        })

        print("Bot:", response)

        # Update memory with this turn
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))


# =====================================================================
# ENTRY POINT — uncomment whichever layer you want to try first
# =====================================================================
if __name__ == "__main__":
    # Start here! Run each one at a time to see the concept build up.

    # layer1_basic_llm_call()
    # layer2_prompt_template()
    # layer3_output_parser()
    # layer4_lcel_chain()
    # layer5_chain_with_memory()

    run_chatbot()   # <-- the full interactive app; run this last