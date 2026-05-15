# Gmail RAG Assistant 📧

An AI-powered Gmail assistant that uses Retrieval-Augmented Generation (RAG) to search, understand, and interact with emails across multiple Gmail accounts.

Built using Streamlit, Gmail API, Sentence Transformers, and Groq LLMs.

---

## Features ✨

- 🔍 Semantic email search using embeddings
- 🤖 AI-powered question answering over emails
- 📬 Multi-account Gmail integration
- 🧠 Local vector embeddings with Sentence Transformers
- ⚡ Fast similarity search with cosine similarity
- 🎯 Cross-encoder re-ranking for better retrieval quality
- ✉️ AI-generated email replies and compositions
- 📤 Send emails directly from the app
- 📊 Modern Streamlit dashboard UI
- 🔐 Secure OAuth2 Gmail authentication

---

## Tech Stack 🛠️

- Python
- Streamlit
- Gmail API
- Sentence Transformers
- Groq API
- NumPy
- Scikit-learn
- HuggingFace Transformers

---

## Project Architecture 📂

```bash
gmail-rag-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── auth/
│   └── gmail_auth.py
│
├── gmail/
│   └── fetch_emails.py
│
├── rag/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── rag_pipeline.py
│   └── vector_store.py
│
├── llm/
│   └── groq_client.py
│
├── config/
│   ├── accounts.py
│   └── settings.py
│
└── models/
```

---

## How It Works ⚙️

1. Connects to Gmail using OAuth2
2. Fetches emails from multiple accounts
3. Chunks email data into smaller contexts
4. Generates embeddings locally using Sentence Transformers
5. Stores vectors in a custom vector store
6. Retrieves relevant email chunks using cosine similarity
7. Re-ranks results using a cross-encoder
8. Sends context to Groq LLM for final answer generation

---

## Setup Instructions 🚀

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/gmail-rag-assistant.git
cd gmail-rag-assistant
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate environment:

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

### 5. Add Gmail OAuth credentials

Place your Google OAuth credentials JSON file in the project root.

Example:

```bash
credentials.json
```

Enable these APIs in Google Cloud Console:

- Gmail API

---

### 6. Run the application

```bash
streamlit run app.py
```

---

## Example Questions 💡

- "Who sent me internship emails?"
- "Summarize unread emails"
- "Any emails about payments?"
- "Show emails related to hackathons"
- "Draft a reply to the latest recruiter email"

---

## Security 🔒

Sensitive files are excluded using `.gitignore`:

- `.env`
- OAuth tokens
- Gmail credentials
- virtual environments
- local embedding models

---

## Future Improvements 🚀

- Conversation memory
- FAISS / ChromaDB integration
- Email summarization dashboard
- Calendar extraction
- Voice assistant support
- Real-time Gmail sync
- Advanced filtering and analytics

---

## Author 👩‍💻

Apeksha Kor

---

## License 📄

This project is for educational and portfolio purposes.