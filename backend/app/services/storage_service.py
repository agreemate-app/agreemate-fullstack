import os
import uuid
from typing import Dict, Optional
from datetime import datetime

class StorageService:
    def __init__(self):
        self.files: Dict[str, bytes] = {}
        self.file_metadata: Dict[str, Dict] = {}
    
    def store_file(self, file_content: bytes, filename: str, content_type: str = "application/pdf") -> str:
        file_id = str(uuid.uuid4())
        file_key = f"{file_id}_{filename}"
        
        self.files[file_key] = file_content
        self.file_metadata[file_key] = {
            "filename": filename,
            "content_type": content_type,
            "size": len(file_content),
            "created_at": datetime.utcnow().isoformat(),
            "file_id": file_id
        }
        
        return file_key
    
    def get_file(self, file_key: str) -> Optional[bytes]:
        return self.files.get(file_key)
    
    def get_file_metadata(self, file_key: str) -> Optional[Dict]:
        return self.file_metadata.get(file_key)
    
    def delete_file(self, file_key: str) -> bool:
        if file_key in self.files:
            del self.files[file_key]
            del self.file_metadata[file_key]
            return True
        return False
    
    def get_file_url(self, file_key: str) -> str:
        return f"/files/{file_key}"

storage_service = StorageService()
