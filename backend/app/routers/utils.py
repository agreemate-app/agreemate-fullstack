from fastapi import APIRouter
from typing import Optional
from app.models.agreement import StampDutyCalculation, AgreementType
from app.services.estamp_service import estamp_service

router = APIRouter(prefix="/utils", tags=["utilities"])

from pydantic import BaseModel

class StampDutyRequest(BaseModel):
    state: str
    agreement_type: AgreementType
    property_value: Optional[float] = None

@router.post("/calculate-stamp-duty", response_model=StampDutyCalculation)
async def calculate_stamp_duty(request: StampDutyRequest):
    calculated_amount = estamp_service.calculate_stamp_duty(request.state, request.agreement_type, request.property_value)
    
    return StampDutyCalculation(
        state=request.state,
        agreement_type=request.agreement_type,
        property_value=request.property_value,
        calculated_amount=calculated_amount
    )

@router.get("/agreement-types")
async def get_agreement_types():
    return {
        "agreement_types": [
            {"value": "rental", "label": "Rental Agreement"},
            {"value": "employment", "label": "Employment Agreement"},
            {"value": "service", "label": "Service Agreement"},
            {"value": "sale", "label": "Sale Agreement"},
            {"value": "partnership", "label": "Partnership Agreement"}
        ]
    }

@router.get("/states")
async def get_states():
    return {
        "states": [
            {"value": "maharashtra", "label": "Maharashtra"},
            {"value": "karnataka", "label": "Karnataka"},
            {"value": "delhi", "label": "Delhi"},
            {"value": "gujarat", "label": "Gujarat"},
            {"value": "tamil_nadu", "label": "Tamil Nadu"},
            {"value": "west_bengal", "label": "West Bengal"},
            {"value": "rajasthan", "label": "Rajasthan"},
            {"value": "uttar_pradesh", "label": "Uttar Pradesh"}
        ]
    }
