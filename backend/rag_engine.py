import os
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document

class RAGEngine:
    def __init__(self):
        self.persist_directory = os.environ.get("CHROMA_DB_DIR", "./chroma_db")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        
        if not self.google_api_key:
            print("WARNING: GOOGLE_API_KEY not found. RAG will not work correctly.")

        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=self.google_api_key)
        self.vector_store = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings
        )
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=self.google_api_key, temperature=0.3)
        
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

    def ingest_documents(self, file_paths: List[str]):
        documents = []
        for path in file_paths:
            if path.endswith(".pdf"):
                loader = PyPDFLoader(path)
                documents.extend(loader.load())
            elif path.endswith(".txt"):
                loader = TextLoader(path)
                documents.extend(loader.load())
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        
        self.vector_store.add_documents(texts)
        self.vector_store.persist()
        print(f"Ingested {len(texts)} chunks.")

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
        
        result = qa_chain({"query": query_text})
        
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
