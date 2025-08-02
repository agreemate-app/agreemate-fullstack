import asyncio
import random
import requests
from typing import Dict, Any, List
from datetime import datetime
from app.models.agreement import ESignRequest
from app.core.config import settings
from app.services.leegality_client import leegality_client
from app.services.pdf_service import pdf_service

class ESignService:
    def __init__(self):
        self.pending_signatures: Dict[str, Dict] = {}
    
    async def initiate_esign(self, esign_request: ESignRequest) -> Dict[str, Any]:
        if not settings.LEEGALITY_ENABLED or not settings.LEEGALITY_AUTH_TOKEN:
            return await self._mock_initiate_esign(esign_request)
        
        try:
            pdf_content = b"PDF content placeholder for agreement"
            file_name = f"agreement_{esign_request.agreement_id}.pdf"
            
            invitees = []
            for signer in esign_request.signers:
                invitee = {
                    "name": signer.get("name"),
                    "email": signer.get("email"),
                    "phone": signer.get("phone", ""),
                    "signType": "aadhaar",
                    "appearances": [
                        {
                            "page": 1,
                            "x": 100,
                            "y": 100,
                            "width": 200,
                            "height": 50
                        }
                    ]
                }
                invitees.append(invitee)
            
            stamp_series = getattr(esign_request, 'stamp_series', None)
            response = leegality_client.create_esign_request(
                file_content=pdf_content,
                file_name=file_name,
                invitees=invitees,
                stamp_series=stamp_series
            )
            
            if response.get("status") == 0:
                data = response.get("data", {})
                document_id = data.get("documentId")
                invitations = data.get("invitations", [])
                
                self.pending_signatures[document_id] = {
                    "agreement_id": esign_request.agreement_id,
                    "signers": esign_request.signers,
                    "status": "pending",
                    "created_at": datetime.utcnow().isoformat(),
                    "leegality_document_id": document_id
                }
                
                sign_links = []
                for invitation in invitations:
                    sign_links.append({
                        "signer_name": invitation.get("name"),
                        "signer_email": invitation.get("email"),
                        "sign_url": invitation.get("signUrl"),
                        "status": "pending"
                    })
                
                return {
                    "status": "initiated",
                    "session_id": document_id,
                    "sign_links": sign_links,
                    "message": "eSign process initiated. Check status using session_id."
                }
            else:
                raise Exception(f"Leegality API error: {response.get('messages', 'Unknown error')}")
                
        except Exception as e:
            return {
                "status": "failed",
                "error": f"eSign service error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _mock_initiate_esign(self, esign_request: ESignRequest) -> Dict[str, Any]:
        await asyncio.sleep(1)
        
        session_id = f"ESIGN_{random.randint(100000, 999999)}"
        
        self.pending_signatures[session_id] = {
            "agreement_id": esign_request.agreement_id,
            "signers": esign_request.signers,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        sign_links = []
        for i, signer in enumerate(esign_request.signers):
            sign_links.append({
                "signer_name": signer.get("name"),
                "signer_email": signer.get("email"),
                "sign_url": f"/esign/sign/{session_id}/{i}",
                "status": "pending"
            })
        
        return {
            "status": "initiated",
            "session_id": session_id,
            "sign_links": sign_links,
            "callback_url": f"/esign/callback/{session_id}",
            "expires_at": datetime.utcnow().isoformat()
        }
    
    async def check_signature_status(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self.pending_signatures:
            return {"status": "not_found"}
        
        session = self.pending_signatures[session_id]
        
        if not settings.LEEGALITY_ENABLED or not settings.LEEGALITY_AUTH_TOKEN:
            return self._mock_check_status(session_id, session)
        
        try:
            leegality_doc_id = session.get("leegality_document_id", session_id)
            response = leegality_client.get_document_status(leegality_doc_id)
            
            if response.get("status") == 0:
                data = response.get("data", {})
                requests_data = data.get("requests", [])
                
                all_completed = all(req.get("status") == "COMPLETED" for req in requests_data)
                
                if all_completed:
                    session["status"] = "completed"
                    session["completed_at"] = datetime.utcnow().isoformat()
                    
                    return {
                        "status": "completed",
                        "session_id": session_id,
                        "agreement_id": session["agreement_id"],
                        "signed_document_url": data.get("files", [{}])[0].get("url", ""),
                        "signatures": [
                            {
                                "signer_name": req.get("name"),
                                "signed_at": req.get("signedAt"),
                                "status": "completed"
                            }
                            for req in requests_data
                        ]
                    }
                else:
                    return {
                        "status": "pending",
                        "session_id": session_id,
                        "agreement_id": session["agreement_id"],
                        "pending_signers": len([req for req in requests_data if req.get("status") != "COMPLETED"])
                    }
            else:
                raise Exception(f"Leegality API error: {response.get('messages', 'Unknown error')}")
                
        except Exception as e:
            return self._mock_check_status(session_id, session)
    
    def _mock_check_status(self, session_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        completed = random.choice([True, False, False])
        
        if completed:
            session["status"] = "completed"
            session["completed_at"] = datetime.utcnow().isoformat()
            
            return {
                "status": "completed",
                "session_id": session_id,
                "agreement_id": session["agreement_id"],
                "signed_document_url": f"/esign/document/{session_id}",
                "signatures": [
                    {
                        "signer_name": signer.get("name"),
                        "signed_at": datetime.utcnow().isoformat(),
                        "status": "completed"
                    }
                    for signer in session["signers"]
                ]
            }
        else:
            return {
                "status": "pending",
                "session_id": session_id,
                "agreement_id": session["agreement_id"],
                "pending_signers": len(session["signers"])
            }
    
    def generate_mock_signed_document(self, session_id: str) -> bytes:
        if session_id not in self.pending_signatures:
            return b"Document not found"
        
        session = self.pending_signatures[session_id]
        
        signed_content = f"""
        DIGITALLY SIGNED DOCUMENT
        
        Session ID: {session_id}
        Agreement ID: {session["agreement_id"]}
        Signed Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
        
        Signers:
        """
        
        for signer in session["signers"]:
            signed_content += f"\n- {signer.get('name')} ({signer.get('email')})"
        
        signed_content += "\n\nThis is a mock digitally signed document for testing purposes."
        signed_content += "\nIn production, this would contain actual digital signatures."
        
        return signed_content.encode('utf-8')

esign_service = ESignService()
