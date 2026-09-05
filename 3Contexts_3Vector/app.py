"""
app.py
------
Streamlit UI for the role-aware CMS assistant.

The user picks a role (Banking / Healthcare / Software Engineer) and asks a
question. The app loads that role's own vector database and retrieves the
answer ONLY from that role's knowledge base, then asks an OpenAI chat model
to generate a grounded answer from the retrieved context.

Run:
    streamlit run app.py

Requires:
    - OPENAI_API_KEY environment variable set
    - vectorstores/ already built by running ingest.py first
"""

import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS, Chroma
from langchain_qdrant import QdrantVectorStore
from langchain_classic.chains import RetrievalQA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstores")

st.set_page_config(page_title="Role-Aware CMS Assistant", page_icon="🤖")

if "OPENAI_API_KEY" not in os.environ:
    st.sidebar.error(
        "OPENAI_API_KEY is not set in your environment.\n\n"
        'Run: export OPENAI_API_KEY="sk-..." before starting Streamlit.'
    )
    st.stop()


@st.cache_resource
def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")


@st.cache_resource
def load_vectorstore(role: str):
    embeddings = get_embeddings()

    if role == "Banking":
        return FAISS.load_local(
            os.path.join(VECTORSTORE_DIR, "banking_faiss"),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    if role == "Healthcare":
        return Chroma(
            collection_name="healthcare_cms",
            embedding_function=embeddings,
            persist_directory=os.path.join(VECTORSTORE_DIR, "healthcare_chroma"),
        )

    if role == "Software Engineer":
        return QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name="software_cms",
            path=os.path.join(VECTORSTORE_DIR, "software_qdrant"),
        )

    raise ValueError(f"Unknown role: {role}")


def get_qa_chain(role: str):
    vectordb = load_vectorstore(role)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )


st.title("🤖 One Question, Three Contexts")
st.caption(
    "Ask 'What is CMS?' and get a different, role-correct answer "
    "depending on who's asking — Banking, Healthcare, or Software Engineering."
)

role = st.selectbox("Select your role", ["Banking", "Healthcare", "Software Engineer"])
question = st.text_input("Ask your question", value="What is CMS?")

if st.button("Get Answer") and question.strip():
    with st.spinner(f"Retrieving the answer from the {role} knowledge base..."):
        try:
            qa_chain = get_qa_chain(role)
            result = qa_chain.invoke({"query": question})

            st.subheader("Answer")
            st.write(result["result"])

            with st.expander("Source chunks used for this answer"):
                for i, doc in enumerate(result["source_documents"], start=1):
                    st.markdown(f"**Chunk {i}:** {doc.page_content[:400]}...")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info(
                "Make sure you've run `python ingest.py` first to build the "
                "vector stores, and that OPENAI_API_KEY is set correctly."
            )
