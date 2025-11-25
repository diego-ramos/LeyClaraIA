import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
from rag_engine import RAGEngine
from youtube_service import search_youtube_videos

app = FastAPI(title="LeyClara.IA API")

# CORS Configuration
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
print(f"DEBUG: CORS allowed_origins = {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from document_store import DocumentStore

# Initialize RAG Engine and Document Store
rag_engine = RAGEngine()
document_store = DocumentStore()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence_score: str
    youtube_videos: List[dict]

from starlette.concurrency import run_in_threadpool

# ...

@app.get("/documents")
def get_documents():
    return document_store.get_all()

import hashlib

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    saved_files = []
    file_hashes = {}
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        # Check if document already exists by name
        if document_store.exists(file.filename):
            raise HTTPException(status_code=400, detail=f"El archivo '{file.filename}' ya existe en la biblioteca.")

        content = await file.read()
        
        # Calculate hash to check for duplicate content
        file_hash = hashlib.md5(content).hexdigest()
        existing_doc = document_store.get_by_hash(file_hash)
        if existing_doc:
            raise HTTPException(status_code=400, detail=f"El contenido de este archivo ya existe (Nombre original: {existing_doc['filename']}).")
        
        file_hashes[file.filename] = file_hash

        file_path = os.path.join(upload_dir, file.filename)
        
        # Debug: Print first 20 bytes
        print(f"File: {file.filename}, Size: {len(content)} bytes, Header: {content[:20]}")

        # Sanitize PDF: Strip leading whitespace if present
        if file.filename.lower().endswith(".pdf"):
            if content.startswith(b'\t') or content.startswith(b'\n') or content.startswith(b'\r') or content.startswith(b' '):
                print("Sanitizing PDF: Removing leading whitespace...")
                content = content.lstrip(b' \t\n\r')

        with open(file_path, "wb") as buffer:
            buffer.write(content)
        saved_files.append(file_path)
    
    # Index documents in a separate thread to avoid blocking the event loop
    try:
        await run_in_threadpool(rag_engine.ingest_documents, saved_files)
        
        # Register in Document Store after successful ingestion
        for file_path in saved_files:
            filename = os.path.basename(file_path)
            document_store.add_document(filename, file_hash=file_hashes.get(filename))
            
        return {"message": f"Successfully processed {len(saved_files)} documents."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 1. Get RAG response (Run in threadpool)
        rag_response = await run_in_threadpool(rag_engine.query, request.message)
        
        # 2. Get YouTube suggestions (Bonus)
        # Extract keywords from the answer or query for better results
        search_query = f"{request.message} legal explanation"
        videos = await run_in_threadpool(search_youtube_videos, search_query)
        
        return ChatResponse(
            answer=rag_response["answer"],
            sources=rag_response["sources"],
            confidence_score=rag_response["confidence_score"],
            youtube_videos=videos
        )
    except Exception as e:
        print(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
