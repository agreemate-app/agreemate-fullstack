import requests
from typing import Dict, Any, Optional
from app.core.config import settings
import base64
import json

class LeegalityClient:
    def __init__(self):
        self.base_url = settings.LEEGALITY_BASE_URL
        self.auth_token = settings.LEEGALITY_AUTH_TOKEN
        self.headers = {
            "X-Auth-Token": self.auth_token,
            "Content-Type": "application/json"
        }
    
    def create_esign_request(self, file_content: bytes, file_name: str, invitees: list, stamp_series: Optional[str] = None) -> Dict[str, Any]:
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        payload = {
            "file": {
                "name": file_name,
                "file": file_base64
            },
            "invitees": invitees,
            "expiryDays": 10,
            "requestSignOrder": True,
            "deleteOnComplete": False
        }
        
        if stamp_series:
            payload["stampSeries"] = stamp_series
        
        response = requests.post(
            f"{self.base_url}/sign/request",
            headers=self.headers,
            json=payload
        )
        
        return response.json()
    
    def get_document_status(self, document_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/sign/request",
            headers=self.headers,
            params={"documentId": document_id}
        )
        
        return response.json()

leegality_client = LeegalityClient()
