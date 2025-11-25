# LeyClara.IA - Walkthrough

This guide explains how to run and verify the **LeyClara.IA** legal chat assistant.

## Prerequisites
- Docker & Docker Compose installed.
- **Google Cloud API Key** (for Gemini LLM).
- **YouTube Data API Key** (for video suggestions).

## Setup & Run

1.  **Environment Variables**:
    Create a `.env` file in the `backend/` directory (or pass them directly to docker-compose).
    ```bash
    GOOGLE_API_KEY=your_google_key
    YOUTUBE_API_KEY=your_youtube_key
    ```

2.  **Start the Application**:
    Run the following command in the root directory:
    ```bash
    docker-compose up --build
    ```
    *This will build the Python backend and the React frontend.*

3.  **Access the App**:
    - **Frontend**: [http://localhost:3000](http://localhost:3000)
    - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Verification Steps

### 1. Ingestion (Upload Documents)
- Open the Frontend.
- Click the **Paperclip** icon.
- Select the dummy documents located in `backend/dummy_docs/`.
- Click **"Subir"**.
- *Verify*: You should see a success message "¡Documentos listos!".

### 2. Chat & RAG
- **Text Query**: Type "Explain the rights of a worker" or "¿Cuáles son los derechos básicos del trabajador?".
- **Voice Query**: Click the **Microphone** icon and speak your question.
- *Verify*:
    - The answer is simple and easy to understand.
    - **Sources**: Click "▶ Ver Fuentes" to see the exact text from `estatuto_trabajadores.txt`.
    - **Confidence**: Check the "Confianza" badge.

### 3. Multimedia
- Check if there are **YouTube Videos** suggested below the answer.

### 4. Voice Output
- Click the **Speaker** icon next to the bot's response to hear it read aloud.
