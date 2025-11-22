import os
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

def test_connection():
    print("--- Starting Connection Test ---")
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY is not set.")
        return

    print(f"API Key found: {api_key[:5]}...{api_key[-5:]}")

    # 1. Test Embedding API (Direct Client)
    print("\n1. Testing Google Embeddings API (Direct)...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Try to list models first (lightweight)
        print("Listing models...")
        for m in genai.list_models():
            if 'embedContent' in m.supported_generation_methods:
                print(f"Found embedding model: {m.name}")
                break
        
        # Try embedding
        print("Generating embedding...")
        result = genai.embed_content(
            model="models/text-embedding-004",
            content="This is a test sentence.",
            task_type="retrieval_document",
            title="Embedding of single string"
        )
        print(f"SUCCESS: Generated embedding vector of length {len(result['embedding'])}")
        
    except Exception as e:
        print(f"FAIL: Embedding API failed. Error: {e}")
        return

    # 2. Test ChromaDB
    print("\n2. Testing ChromaDB (Write/Read)...")
    try:
        # Re-initialize embeddings for LangChain/Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)

        persist_directory = os.environ.get("CHROMA_DB_DIR", "./chroma_db")
        vector_store = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
        
        doc = Document(page_content="Test document content", metadata={"source": "test_script"})
        vector_store.add_documents([doc])
        vector_store.persist()
        print("SUCCESS: Wrote document to ChromaDB.")
        
        # Query back
        results = vector_store.similarity_search("Test document", k=1)
        if results:
            print(f"SUCCESS: Retrieved document: {results[0].page_content}")
        else:
            print("FAIL: Could not retrieve document from ChromaDB.")
            
    except Exception as e:
        print(f"FAIL: ChromaDB operation failed. Error: {e}")
        return

    print("\n--- Test Completed Successfully ---")

if __name__ == "__main__":
    test_connection()
