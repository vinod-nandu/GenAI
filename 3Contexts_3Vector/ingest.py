"""
ingest.py
---------
Loads 3 role-specific documents, splits them into chunks, embeds them with
OpenAI embeddings, and stores each role's chunks in its OWN vector database:

    Banking            -> FAISS   (vectorstores/banking_faiss)
    Healthcare         -> Chroma  (vectorstores/healthcare_chroma)
    Software Engineer  -> Qdrant  (vectorstores/software_qdrant, local mode)

Run this once (or whenever the source docs change) before starting app.py.

Requires the OPENAI_API_KEY environment variable to be set:
    export OPENAI_API_KEY="sk-..."          (macOS/Linux)
    setx OPENAI_API_KEY "sk-..."            (Windows)
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_qdrant import QdrantVectorStore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. Export it before running ingest.py, e.g.\n"
        '  export OPENAI_API_KEY="sk-..."'
    )

DOCS = {
    "Banking": os.path.join(BASE_DIR, "docs", "banking_cms.txt"),
    "Healthcare": os.path.join(BASE_DIR, "docs", "healthcare_cms.txt"),
    "Software Engineer": os.path.join(BASE_DIR, "docs", "software_cms.txt"),
}
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstores")


def load_and_split(path: str):
    """Load a text file and split it into overlapping chunks for embedding."""
    loader = TextLoader(path, encoding="utf-8")
    raw_docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(raw_docs)


def build_stores():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    # 1. Banking -> FAISS
    print("Building Banking vector store (FAISS)...")
    banking_chunks = load_and_split(DOCS["Banking"])
    banking_store = FAISS.from_documents(banking_chunks, embeddings)
    banking_store.save_local(os.path.join(VECTORSTORE_DIR, "banking_faiss"))
    print(f"  -> {len(banking_chunks)} chunks stored.")

    # 2. Healthcare -> Chroma
    print("Building Healthcare vector store (Chroma)...")
    health_chunks = load_and_split(DOCS["Healthcare"])
    health_store = Chroma.from_documents(
        health_chunks,
        embeddings,
        collection_name="healthcare_cms",
        persist_directory=os.path.join(VECTORSTORE_DIR, "healthcare_chroma"),
    )
    health_store.persist()
    print(f"  -> {len(health_chunks)} chunks stored.")

    # 3. Software Engineer -> Qdrant (local/embedded mode, no server required)
    print("Building Software Engineer vector store (Qdrant)...")
    sw_chunks = load_and_split(DOCS["Software Engineer"])
    QdrantVectorStore.from_documents(
        sw_chunks,
        embeddings,
        collection_name="software_cms",
        path=os.path.join(VECTORSTORE_DIR, "software_qdrant"),
    )
    print(f"  -> {len(sw_chunks)} chunks stored.")

    print("\nAll 3 role-specific vector stores built successfully.")


if __name__ == "__main__":
    build_stores()