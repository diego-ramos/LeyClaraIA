import os
import hashlib
from datetime import datetime
from document_store import DocumentStore

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_database():
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        print(f"Directory '{upload_dir}' not found.")
        return

    store = DocumentStore()
    count = 0
    
    print("Starting synchronization...")
    
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        
        if os.path.isfile(file_path):
            # Calculate hash
            file_hash = calculate_md5(file_path)
            
            # Check if already in DB (by hash or filename)
            if store.get_by_hash(file_hash):
                print(f"Skipping {filename} (already indexed by hash).")
                continue
                
            if store.exists(filename):
                print(f"Skipping {filename} (already indexed by name).")
                # Optional: Update hash if missing? For now, just skip.
                continue

            # Add to DB
            print(f"Adding {filename}...")
            store.add_document(filename, file_hash)
            count += 1

    print(f"\nSync complete. Added {count} new documents to the database.")

if __name__ == "__main__":
    sync_database()
