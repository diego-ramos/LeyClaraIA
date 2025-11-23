import os
from datetime import datetime
from tinydb import TinyDB, Query

class DocumentStore:
    def __init__(self, db_path="/data/documents.json"):
        self.db = TinyDB(db_path)
        self.documents = self.db.table('documents')

    def add_document(self, filename: str, file_hash: str = None):
        """Adds a document to the store with the current timestamp and optional hash."""
        # Check if filename exists to avoid duplicates by name (optional, but good for consistency)
        if not self.exists(filename):
            self.documents.insert({
                'filename': filename,
                'file_hash': file_hash,
                'upload_date': datetime.now().isoformat()
            })

    def exists(self, filename: str) -> bool:
        """Checks if a document with the given filename already exists."""
        Doc = Query()
        return self.documents.contains(Doc.filename == filename)

    def get_by_hash(self, file_hash: str):
        """Returns the document if a file with the given hash exists."""
        if not file_hash:
            return None
        Doc = Query()
        result = self.documents.search(Doc.file_hash == file_hash)
        return result[0] if result else None

    def get_all(self):
        """Returns all documents in the store."""
        return self.documents.all()
