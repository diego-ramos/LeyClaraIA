import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
from rag_engine import RAGEngine
from youtube_service import search_youtube_videos

app = FastAPI(title="TeLoExplico API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
rag_engine = RAGEngine()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence_score: str
    youtube_videos: List[dict]

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    saved_files = []
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)
    
    # Index documents
    try:
        rag_engine.ingest_documents(saved_files)
        return {"message": f"Successfully processed {len(saved_files)} documents."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 1. Get RAG response
        rag_response = rag_engine.query(request.message)
        
        # 2. Get YouTube suggestions (Bonus)
        # Extract keywords from the answer or query for better results
        search_query = f"{request.message} legal explanation"
        videos = search_youtube_videos(search_query)
        
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
