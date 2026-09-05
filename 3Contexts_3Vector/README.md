# One Question, Three Contexts — Role-Aware CMS Assistant

A small LangChain + Streamlit demo showing how the *same* question ("What is
CMS?") should be answered differently depending on the role of the person
asking — Banking, Healthcare, or Software Engineer — by routing retrieval to
a **separate vector database per role**:

| Role               | Vector DB | Meaning of "CMS" retrieved                     |
|--------------------|-----------|--------------------------------------------------|
| Banking            | FAISS     | Cash Management System / Card Management System |
| Healthcare         | Chroma    | Centers for Medicare & Medicaid Services         |
| Software Engineer  | Qdrant (local mode) | Content Management System              |

## Project structure

```
cms_role_rag/
├── docs/
│   ├── banking_cms.txt
│   ├── healthcare_cms.txt
│   └── software_cms.txt
├── vectorstores/          # created automatically by ingest.py
├── ingest.py              # builds the 3 role-specific vector stores
├── app.py                 # Streamlit UI
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key as an environment variable (never hardcode it in
   the code):
   ```bash
   export OPENAI_API_KEY="sk-..."          # macOS / Linux
   setx OPENAI_API_KEY "sk-..."            # Windows (new terminal after)
   ```

3. Build the 3 vector stores (run once, or again if you edit the docs):
   ```bash
   python ingest.py
   ```

4. Launch the app:
   ```bash
   streamlit run app.py
   ```

5. In the UI, pick a role from the dropdown, ask "What is CMS?" (or any of
   the sample questions inside each doc), and see the role-correct answer
   retrieved from that role's own vector database.

## Extending this to production: multi-application support

The exact same pattern generalizes beyond "roles" to **applications**. Swap
the role dropdown for an application dropdown (App1 / App2 / App3), give
each application its own document set (server IPs, background services,
runbooks, on-call procedures) and its own vector store, and you get a
production-ready assistant that correctly answers questions like:

- "What is your webserver IP?"
- "What all services are running in the background server?"

...without ever mixing up App1's infrastructure with App3's. Just repeat
the same ingest → embed → store → retrieve-by-selector pattern used here,
one more time, per application.

## Notes

- This demo uses three different vector database technologies (FAISS,
  Chroma, Qdrant) purely to illustrate LangChain's flexibility. In a real
  production system you would typically pick ONE vector database technology
  and isolate roles/applications using separate collections, namespaces, or
  metadata filters — that's usually simpler to operate than mixing vendors.
- LangChain and vector DB client APIs evolve quickly; if a method signature
  in this code doesn't match your installed version, check that library's
  current documentation.
