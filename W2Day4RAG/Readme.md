B11 | W2 | Day 2 | RAG - PDF AI Assiatance

AIM 

Build a RAG (Retrieval-Augmented Generation) app using LangChain for the retrieval pipeline
and Streamlit for the user interface. The user uploads a PDF in the browser. As soon as it is
uploaded, your app reads the PDF, splits it into chunks, turns them into embeddings, and stores
them in a vector database. Once that database is ready, the user can ask questions and get
answers that are grounded in the contents of their PDF.


Criteria 

Show a Streamlit interface with a PDF file uploader.
• When a PDF is uploaded, load it, split it into chunks, create embeddings, and store them in a
vector database (for example, FAISS or Chroma) so the database is ready to search.
• Give the user a query box to ask questions about the uploaded PDF.
• Use LangChain retrieval together with an OpenAI model to answer from the PDF content.
• Display the answer clearly in the app.
• Read your API key from an environment variable - never hard-code or commit it.
• Keep all your code in a single file named app.py
