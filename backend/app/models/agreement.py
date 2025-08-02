from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class AgreementType(str, Enum):
    RENTAL = "rental"
    EMPLOYMENT = "employment"
    SERVICE = "service"
    SALE = "sale"
    PARTNERSHIP = "partnership"

class DocumentStatus(str, Enum):
    DRAFT = "draft"
    ESTAMP_PENDING = "estamp_pending"
    ESTAMP_COMPLETED = "estamp_completed"
    ESIGN_PENDING = "esign_pending"
    ESIGN_COMPLETED = "esign_completed"
    COMPLETED = "completed"
    FAILED = "failed"

class AgreementBase(BaseModel):
    title: str
    agreement_type: AgreementType
    template_data: Dict[str, Any]
    parties: List[Dict[str, str]]
    state: str
    stamp_duty_amount: Optional[float] = None

class AgreementCreate(AgreementBase):
    pass

class AgreementUpdate(BaseModel):
    title: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    parties: Optional[List[Dict[str, str]]] = None
    state: Optional[str] = None

class Agreement(AgreementBase):
    id: str
    user_id: str
    status: DocumentStatus = DocumentStatus.DRAFT
    created_at: datetime
    updated_at: datetime
    estamp_certificate_url: Optional[str] = None
    esign_document_url: Optional[str] = None
    final_document_url: Optional[str] = None
    stamp_series: Optional[str] = None
    activity_log: List[Dict[str, Any]] = []
    
    class Config:
        from_attributes = True

class StampDutyCalculation(BaseModel):
    state: str
    agreement_type: AgreementType
    property_value: Optional[float] = None
    calculated_amount: float
    
class EStampRequest(BaseModel):
    agreement_id: str
    state: str
    agreement_type: str
    stamp_duty_amount: float

class ESignRequest(BaseModel):
    agreement_id: str
    signers: List[Dict[str, str]]
    stamp_series: Optional[str] = None
