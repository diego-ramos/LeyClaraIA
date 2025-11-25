# LeyClara.IA 📜⚖️

[![es](https://img.shields.io/badge/lang-es-yellow.svg)](README.md)


**LeyClara.IA** is an intelligent legal assistant designed to democratize access to legal information. Its goal is to take complex legal documents (laws, contracts, judgments) and explain them in simple, accessible language for anyone, "like I'm 5 years old".

## 🧠 Technical Architecture: RAG (Retrieval-Augmented Generation)

This project uses a **RAG** architecture instead of a simple AI chat.

### Why RAG?
Large Language Models (LLMs) like GPT or Gemini have two major limitations:
1.  **Hallucinations:** They can invent data if they don't know the answer.
2.  **Lack of Knowledge:** They don't know your private documents or specific local laws that weren't in their training data.

RAG solves this by allowing the AI to "read" your documents before answering. The flow is:
1.  **Retrieval:** The system searches your library for the exact paragraphs that answer your question.
2.  **Augmented Generation:** It sends those paragraphs to the AI and says: *"Use ONLY this information to answer the user"*. This guarantees accurate answers based on real evidence.

## 📚 The Role of ChromaDB (Our "Library")

To make the system fast and efficient, we use **ChromaDB**, a vector database.

*   **The Problem:** We can't send a 500-page PDF to the AI every time we ask a question. It would be slow, expensive, and exceed the model's memory context.
*   **The Solution (ChromaDB):**
    1.  When you upload a PDF, we "cut" it into small pieces.
    2.  We convert each piece into a "mathematical fingerprint" (vector) using the Google Embeddings API.
    3.  We save these vectors locally in ChromaDB.
    4.  When you ask a question, ChromaDB mathematically finds the 6 fragments most similar to your question in milliseconds, without having to re-read the entire document.

## ✂️ Chunking Strategy (Fragmentation)

A critical design decision was the size of the "chunks" (text fragments).

*   **Current Configuration:** 500 characters (with 100 overlap).
*   **Why this size?**
    *   Initially, we tested with 1000 characters, but the system lost specific details (like article numbers or short titles) because they were "diluted" in so much text.
    *   By reducing it to **500 characters**, we achieved a "magnifying glass" effect: each fragment is more specific and precise. This allows finding "needles in a haystack" (specific details) much more effectively.

## 🧩 The Role of LangChain (The "Glue")

**LangChain** is the framework that connects all the pieces of the puzzle. It acts as the orchestrator that:

1.  **Loads and Processes:** Uses tools to read PDFs and split them into chunks.
2.  **Connects:** Bridges your local database (ChromaDB) and the Google API (Gemini).
3.  **Manages the Flow:** When you ask a question, LangChain automatically executes a "chain" of steps: search context -> build prompt -> query AI -> deliver answer.

Without LangChain, we would have to manually write all the code to connect these disparate services.

## 🛠️ Technologies

*   **Backend:** Python, FastAPI.
*   **AI:** Google Gemini 1.5 Flash (via LangChain).
*   **Database:** ChromaDB (Vector Store).
*   **Frontend:** React, TailwindCSS.
*   **Infrastructure:** Docker & Docker Compose.

## 🚀 How to Run It

### Local Development

1.  Clone the repository.
2.  Create a `.env` file in the root with your API keys (see `.env.example`).
3.  Create a `frontend/.env` file with:
    ```env
    VITE_API_URL=http://localhost:8000
    ```
4.  Run:
    ```bash
    docker-compose up --build
    ```
5.  Open `http://localhost:3000` and start uploading documents.

### 🌐 Cloud Deployment

#### Option 1: Google Compute Engine (Recommended - With Persistence)

For production deployment with persistent storage:

```bash
# See full instructions
cat .agent/workflows/deploy-to-gce.md
```

**Advantages:**
- ✅ Persistent data (ChromaDB, uploaded documents)
- ✅ Predictable costs (~$15-30/month)
- ✅ Full server control

#### Option 2: Railway

Railway offers $5/month of free credit, enough for small/medium projects.

**Quick Guide:**
1. Create an account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Follow the guide: [`RAILWAY_DEPLOY.md`](RAILWAY_DEPLOY.md)
4. Use the checklist: [`RAILWAY_CHECKLIST.md`](RAILWAY_CHECKLIST.md)

**Resources:**
- 📖 [Complete Deployment Guide](.agent/workflows/deploy_to_railway.md)
- 🔧 [Environment Variables](RAILWAY_ENV_VARS.md)
- ✅ [Deployment Checklist](RAILWAY_CHECKLIST.md)

#### Option 3: Google Cloud Run (Stateless)

For quick deployment without persistence:

```bash
# See instructions
cat .agent/workflows/deploy_to_cloud_run.md
```

**Limitations:**
- ⚠️ Data is lost on restart
- ⚠️ Not recommended for production

#### Other Options

- **Render**: Free alternative similar to Railway
- **Fly.io**: Excellent for Docker applications
