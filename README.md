# 🧠 RagBot 2.0 — AI-Powered PDF Chat Assistant

A modular **Retrieval-Augmented Generation (RAG)** application that lets users upload PDF documents and chat with an AI assistant. Built with a decoupled **FastAPI backend** and **Streamlit frontend**, using **Pinecone** as the vector store and **Groq's LLaMA3** as the LLM.

---

## ✨ Features

- 📄 Upload and parse PDF documents
- 🧠 Embed document chunks with sentence-transformers
- 🗂️ Store embeddings in Pinecone vector database
- 💬 Query documents using LLaMA 3.1 (8B) via Groq
- 🌐 Microservice architecture (Streamlit + FastAPI)
- 📥 Export chat history (TXT/JSON)
- 🎨 Modern, responsive UI

---

## 📂 Project Structure

```
RagBot-2.0/
├── client/                 # Streamlit Frontend
│   ├── components/
│   │   ├── chatUI.py
│   │   ├── history_download.py
│   │   └── upload.py
│   ├── utils/
│   │   └── api.py
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
├── server/                 # FastAPI Backend
│   ├── modules/
│   │   ├── load_vectorstore.py
│   │   ├── llm.py
│   │   ├── pdf_handlers.py
│   │   └── query_handlers.py
│   ├── logger.py
│   ├── main.py
│   ├── .env.example
│   └── requirements.txt
├── Dockerfile
├── start.sh
└── README.md
```

---

## 🚀 Getting Started (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/tarun89034/Rag_bot.git
cd Rag_bot
```

### 2. Setup the Backend (FastAPI)

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_key
PINECONE_API_KEY=your_pinecone_key
```

```bash
uvicorn main:app --reload
```

### 3. Setup the Frontend (Streamlit)

```bash
cd ../client
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload_pdfs/` | Upload PDFs and index into Pinecone |
| `POST` | `/ask/` | Send a query and receive AI-powered answer |
| `GET` | `/test` | Health check |
| `GET` | `/docs` | Swagger API documentation |

---

## 🐳 Docker Deployment

```bash
docker build -t ragbot .
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  -e GOOGLE_API_KEY=your_key \
  ragbot
```

Access the app at `http://localhost:8000`

---

## ☁️ Deploy to Hugging Face Spaces (No Credit Card Required)

1. Push this repo to GitHub.
2. Go to [Hugging Face Spaces](https://huggingface.co/new-space).
3. Name your space and select **Docker** as the SDK.
4. Choose the **Blank** template or **Standard** Docker.
5. In the **Settings** tab of your Space, add your secrets:
   - `GROQ_API_KEY`
   - `PINECONE_API_KEY`
   - `GOOGLE_API_KEY`
6. Hugging Face will automatically build and deploy your Dockerfile.
7. Access the app at the provided Space URL.

Note: The app is configured to listen on port **7860**, which is the default for Hugging Face Spaces.

---

## 🔑 Required API Keys

| Service | Get Key From |
|---------|-------------|
| Groq | [console.groq.com](https://console.groq.com) |
| Pinecone | [pinecone.io](https://www.pinecone.io) |
| Google AI | [AI Studio](https://makersuite.google.com/app/apikey) |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, LangChain, Pinecone, Groq (LLaMA 3.1)
- **Frontend:** Streamlit
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Deployment:** Docker, Koyeb

---

## 📜 License

MIT License

---

> Built with ❤️ using LangChain, Pinecone, Groq & Streamlit
