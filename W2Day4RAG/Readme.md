# AIM

Build a **RAG (Retrieval-Augmented Generation)** application using:

- **LangChain** for the retrieval pipeline
- **Streamlit** for the user interface
- **OpenAI** for embeddings and question answering
- **Chroma** or **FAISS** as the vector database

The user uploads a PDF through the browser. Once uploaded, the application:

1. Reads the PDF.
2. Extracts the text.
3. Splits the text into chunks.
4. Generates embeddings for the chunks.
5. Stores the embeddings in a vector database.
6. Allows the user to ask questions about the PDF.
7. Retrieves relevant content from the PDF.
8. Uses an OpenAI model to generate an answer grounded in the retrieved content.

---

# Criteria

- Show a **Streamlit interface** with a PDF file uploader.
- When a PDF is uploaded:
  - Load the PDF.
  - Split the text into chunks.
  - Create embeddings.
  - Store the embeddings in a vector database such as **FAISS** or **Chroma**.
- Provide a **query box** for users to ask questions about the uploaded PDF.
- Use **LangChain retrieval** together with an **OpenAI model** to answer questions based on the PDF content.
- Display the generated answer clearly in the Streamlit application.
- Read the **OpenAI API key from an environment variable**.
- Never hard-code or commit the API key.
- Keep all application code in a single file:

```text
app.py
