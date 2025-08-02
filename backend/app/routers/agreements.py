from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from typing import List
import io
from app.models.user import User
from app.models.agreement import Agreement, AgreementCreate, AgreementUpdate, DocumentStatus, EStampRequest, ESignRequest
from app.routers.auth import get_current_user
from app.database import db
from app.services.template_service import template_service
from app.services.pdf_service import pdf_service
from app.services.storage_service import storage_service
from app.services.estamp_service import estamp_service
from app.services.esign_service import esign_service

router = APIRouter(prefix="/agreements", tags=["agreements"])

@router.post("/", response_model=Agreement)
async def create_agreement(
    agreement_create: AgreementCreate,
    current_user: User = Depends(get_current_user)
):
    agreement = db.create_agreement(current_user.id, agreement_create)
    return agreement

@router.get("/{agreement_id}", response_model=Agreement)
async def get_agreement(
    agreement_id: str,
    current_user: User = Depends(get_current_user)
):
    agreement = db.get_agreement(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    
    if agreement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this agreement")
    
    return agreement

@router.put("/{agreement_id}", response_model=Agreement)
async def update_agreement(
    agreement_id: str,
    agreement_update: AgreementUpdate,
    current_user: User = Depends(get_current_user)
):
    agreement = db.get_agreement(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    
    if agreement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this agreement")
    
    if agreement.status != DocumentStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Can only update draft agreements")
    
    updated_agreement = db.update_agreement(agreement_id, agreement_update)
    return updated_agreement

@router.post("/{agreement_id}/estamp")
async def request_estamp(
    agreement_id: str,
    current_user: User = Depends(get_current_user)
):
    agreement = db.get_agreement(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    
    if agreement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if agreement.status != DocumentStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Agreement must be in draft status")
    
    db.update_agreement_status(agreement_id, DocumentStatus.ESTAMP_PENDING)
    
    estamp_request = EStampRequest(
        agreement_id=agreement_id,
        state=agreement.state,
        agreement_type=agreement.agreement_type.value,
        stamp_duty_amount=agreement.stamp_duty_amount or 100
    )
    
    result = await estamp_service.request_estamp(estamp_request)
    
    if result["status"] == "success":
        agreement.estamp_certificate_url = result["certificate_url"]
        stamp_series = result.get("stamp_series")
        if stamp_series:
            agreement.stamp_series = stamp_series
        
        db.update_agreement_status(agreement_id, DocumentStatus.ESTAMP_COMPLETED, {
            "estamp_id": result["estamp_id"],
            "certificate_url": result["certificate_url"],
            "stamp_series": stamp_series
        })
        
        estamp_cert = estamp_service.generate_mock_estamp_certificate(agreement_id)
        cert_key = storage_service.store_file(estamp_cert, f"estamp_{agreement_id}.txt", "text/plain")
        agreement.estamp_certificate_url = storage_service.get_file_url(cert_key)
        
        return {"status": "success", "message": "eStamp completed successfully"}
    else:
        db.update_agreement_status(agreement_id, DocumentStatus.FAILED, {
            "error": result["error"]
        })
        raise HTTPException(status_code=400, detail=result["error"])

@router.post("/{agreement_id}/esign")
async def request_esign(
    agreement_id: str,
    current_user: User = Depends(get_current_user)
):
    agreement = db.get_agreement(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    
    if agreement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if agreement.status != DocumentStatus.ESTAMP_COMPLETED:
        raise HTTPException(status_code=400, detail="Agreement must have completed eStamp process")
    
    db.update_agreement_status(agreement_id, DocumentStatus.ESIGN_PENDING)
    
    esign_request = ESignRequest(
        agreement_id=agreement_id,
        signers=agreement.parties,
        stamp_series=getattr(agreement, 'stamp_series', None)
    )
    
    result = await esign_service.initiate_esign(esign_request)
    
    if result["status"] == "initiated":
        return {
            "status": "initiated",
            "session_id": result["session_id"],
            "sign_links": result["sign_links"],
            "message": "eSign process initiated. Check status using session_id."
        }
    else:
        db.update_agreement_status(agreement_id, DocumentStatus.FAILED)
        raise HTTPException(status_code=400, detail="Failed to initiate eSign process")

@router.get("/{agreement_id}/esign-status/{session_id}")
async def check_esign_status(
    agreement_id: str,
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    agreement = db.get_agreement(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    
    if agreement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await esign_service.check_signature_status(session_id)
    
    if result["status"] == "completed":
        signed_doc = esign_service.generate_mock_signed_document(session_id)
        doc_key = storage_service.store_file(signed_doc, f"signed_{agreement_id}.txt", "text/plain")
        agreement.esign_document_url = storage_service.get_file_url(doc_key)
        
        db.update_agreement_status(agreement_id, DocumentStatus.ESIGN_COMPLETED, {
            "session_id": session_id,
            "signed_document_url": result["signed_document_url"]
        })
        
        db.update_agreement_status(agreement_id, DocumentStatus.COMPLETED)
    
    return result

@router.get("/{agreement_id}/pdf")
async def download_pdf(
    agreement_id: str,
    current_user: User = Depends(get_current_user)
):
    agreement = db.get_agreement(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    
    if agreement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    pdf_content = pdf_service.generate_agreement_pdf(
        agreement.agreement_type,
        agreement.template_data,
        agreement_id
    )
    
    pdf_key = storage_service.store_file(pdf_content, f"agreement_{agreement_id}.pdf")
    agreement.final_document_url = storage_service.get_file_url(pdf_key)
    
    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=agreement_{agreement_id}.pdf"}
    )

@router.get("/", response_model=List[Agreement])
async def list_agreements(current_user: User = Depends(get_current_user)):
    agreements = db.get_user_agreements(current_user.id)
    return agreements
