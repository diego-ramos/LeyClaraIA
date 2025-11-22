import os
import pypdf
import time
import random
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

class CustomGoogleEmbeddings(Embeddings):
    def __init__(self, api_key, model="models/text-embedding-004"):
        genai.configure(api_key=api_key, transport='rest')
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']

class RAGEngine:
    def __init__(self):
        self.persist_directory = os.environ.get("CHROMA_DB_DIR", "./chroma_db")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        
        if not self.google_api_key:
            print("WARNING: GOOGLE_API_KEY not found. RAG will not work correctly.")
        
        # Use custom embeddings class to force REST transport and bypass LangChain wrapper issues
        self.embeddings = CustomGoogleEmbeddings(api_key=self.google_api_key, model="models/text-embedding-004")
        
        self.vector_store = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings
        )
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=self.google_api_key, temperature=0.3)
        
        # Custom Prompt for "Explain like I'm 5"
        self.prompt_template = """
        You are a helpful legal assistant. Your goal is to explain complex legal concepts to a non-expert user in simple, easy-to-understand language (like explaining to a 5-year-old, but respectful).
        
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer (in simple terms):
        """
        self.prompt = PromptTemplate(
            template=self.prompt_template, input_variables=["context", "question"]
        )

    def retry_with_backoff(self, func, *args, max_retries=8, **kwargs):
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "504" in str(e) or "Deadline Exceeded" in str(e):
                    wait_time = (2 ** i) + random.random()
                    print(f"API Timeout (504). Retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    raise e
        raise Exception("Max retries exceeded for API call")

    def ingest_documents(self, file_paths: List[str]):
        documents = []
        for path in file_paths:
            if path.endswith(".pdf"):
                try:
                    print(f"Starting to read PDF: {path}")
                    # Use pypdf directly with strict=False for better tolerance
                    reader = pypdf.PdfReader(path, strict=False)
                    text = ""
                    total_pages = len(reader.pages)
                    print(f"PDF has {total_pages} pages.")
                    
                    for i, page in enumerate(reader.pages):
                        print(f"Extracting page {i+1}/{total_pages}...")
                        page_text = page.extract_text() or ""
                        text += page_text
                    
                    print(f"Finished extracting text from {path}. Length: {len(text)} chars.")
                    documents.append(Document(page_content=text, metadata={"source": path}))
                    print(f"Successfully loaded PDF: {path}")
                except Exception as e:
                    print(f"Error loading PDF {path}: {e}")
            elif path.endswith(".txt"):
                loader = TextLoader(path)
                documents.extend(loader.load())
        
        if not documents:
            print("No documents to index.")
            return

        print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        
        print(f"Generated {len(texts)} chunks. Starting embedding in batches...")
        
        # Batch processing to avoid API timeouts
        batch_size = 1
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size} ({len(batch)} chunks)...")
            
            # Retry embedding generation for each batch
            self.retry_with_backoff(self.vector_store.add_documents, batch)
            time.sleep(1.5) # Rate limiting
            
        self.vector_store.persist()
        print(f"Ingested {len(texts)} chunks successfully.")

    def query(self, query_text: str) -> Dict:
        # Retrieve top k documents
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        # Create Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        
        # Retry query execution
        result = self.retry_with_backoff(qa_chain, {"query": query_text})
        
        answer = result["result"]
        source_docs = result["source_documents"]
        
        # Format sources
        formatted_sources = []
        for doc in source_docs:
            formatted_sources.append({
                "content": doc.page_content[:200] + "...", # Snippet
                "source": os.path.basename(doc.metadata.get("source", "Unknown")),
                "page": doc.metadata.get("page", 0)
            })
            
        # Mock confidence score for now (Gemini doesn't always return logprobs easily via LangChain)
        # In a real scenario, we'd check the retrieval scores or ask the LLM to rate its confidence.
        confidence_score = "High" if len(source_docs) > 0 else "Low"
        
        return {
            "answer": answer,
            "sources": formatted_sources,
            "confidence_score": confidence_score
        }
