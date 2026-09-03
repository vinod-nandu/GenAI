import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import tempfile

# 1. Page Configuration
st.set_page_config(page_title="PDF RAG Assistant", page_icon="📄")
header_image = os.path.join(os.path.dirname(__file__), "1788448205.png")
st.image(header_image, use_container_width=True)
st.title("📄 PDF Question-Answering Assistant")
st.write("Upload a PDF document to parse, embed, and query its contents using RAG.")

# 2. Safety Check for OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing `OPENAI_API_KEY` environment variable. Please set it before running the app.")
    st.stop()

# 3. File Uploader Interface
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Use session state to cache the vector database initialization per file
    if "vector_store" not in st.session_state or st.session_state.get("file_name") != uploaded_file.name:
        with st.spinner("Processing PDF: Extracting, splitting, and generating embeddings..."):
            try:
                # Streamlit uploaded file is an in-memory byte stream. 
                # PyPDFLoader needs a file path, so we write to a temporary file safely.
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name

                # Load the PDF content
                loader = PyPDFLoader(tmp_file_path)
                documents = loader.load()

                # Clean up the temporary file from the disk
                os.remove(tmp_file_path)

                # Split document text into chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = text_splitter.split_documents(documents)

                # Initialize OpenAI Embeddings 
                embeddings = OpenAIEmbeddings(openai_api_key=api_key)

                # Store text chunks in a temporary in-memory Chroma database
                vector_store = Chroma.from_documents(chunks, embeddings)
                
                # Save status in session state
                st.session_state["vector_store"] = vector_store
                st.session_state["file_name"] = uploaded_file.name
                st.success("Database ready! Your document has been successfully indexed.")

            except Exception as e:
                st.error(f"An error occurred while parsing the file: {e}")
                st.stop()

    # 4. Query Box and Answer Retrieval Interface
    st.divider()
    user_query = st.text_input("Ask a question about the contents of your PDF:")

    if user_query:
        with st.spinner("Searching database and drafting answer..."):
            try:
                # Use the initialized vector store from session state
                vector_store = st.session_state["vector_store"]
                retriever = vector_store.as_retriever(search_kwargs={"k": 4})

                # Initialize the OpenAI model
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

                # Define the prompt formatting rule
                system_prompt = (
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer "
                    "the question. If you don't know the answer, say that you "
                    "don't know.\n\n"
                    "Context:\n{context}"
                )
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])

                # Construct the Retrieval Chain
                question_answer_chain = create_stuff_documents_chain(llm, prompt)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)

                # Execute query pipeline
                response = rag_chain.invoke({"input": user_query})

                # Display the grounded answer output
                st.markdown("### Answer")
                st.write(response["answer"])

            except Exception as e:
                st.error(f"An error occurred while generating the answer: {e}")
