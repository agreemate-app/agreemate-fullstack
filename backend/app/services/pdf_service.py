from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import base64
from typing import Dict, Any
from app.models.agreement import AgreementType

class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
    
    def generate_pdf_from_html(self, html_content: str, agreement_id: str) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        story.append(Paragraph(html_content, self.styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_agreement_pdf(self, agreement_type: AgreementType, template_data: Dict[str, Any], agreement_id: str) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        
        if agreement_type == AgreementType.RENTAL:
            story.append(Paragraph("RENTAL AGREEMENT", self.title_style))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(f"<b>Landlord:</b> {template_data.get('landlordName', '[Landlord Name]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Address:</b> {template_data.get('landlordAddress', '[Landlord Address]')}", self.styles['Normal']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(f"<b>Tenant:</b> {template_data.get('tenantName', '[Tenant Name]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Address:</b> {template_data.get('tenantAddress', '[Tenant Address]')}", self.styles['Normal']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(f"<b>Property Address:</b> {template_data.get('propertyAddress', '[Property Address]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Monthly Rent:</b> ₹{template_data.get('rentAmount', '[Rent Amount]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Security Deposit:</b> ₹{template_data.get('securityDeposit', '[Security Deposit]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Lease Period:</b> {template_data.get('startDate', '[Start Date]')} to {template_data.get('endDate', '[End Date]')}", self.styles['Normal']))
            
        elif agreement_type == AgreementType.EMPLOYMENT:
            story.append(Paragraph("EMPLOYMENT AGREEMENT", self.title_style))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(f"<b>Employer:</b> {template_data.get('employerName', '[Employer Name]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Employee:</b> {template_data.get('employeeName', '[Employee Name]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Position:</b> {template_data.get('position', '[Position]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Annual Salary:</b> ₹{template_data.get('salary', '[Salary]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Start Date:</b> {template_data.get('startDate', '[Start Date]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Work Location:</b> {template_data.get('workLocation', '[Work Location]')}", self.styles['Normal']))
            
        else:
            story.append(Paragraph("SERVICE AGREEMENT", self.title_style))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(f"<b>Service Provider:</b> {template_data.get('serviceProviderName', '[Service Provider]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Client:</b> {template_data.get('clientName', '[Client Name]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Service Description:</b> {template_data.get('serviceDescription', '[Service Description]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Service Amount:</b> ₹{template_data.get('serviceAmount', '[Service Amount]')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Duration:</b> {template_data.get('startDate', '[Start Date]')} to {template_data.get('endDate', '[End Date]')}", self.styles['Normal']))
        
        story.append(Spacer(1, 24))
        story.append(Paragraph(f"<b>Agreement ID:</b> {agreement_id}", self.styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def merge_estamp_certificate(self, original_pdf: bytes, estamp_pdf: bytes) -> bytes:
        return original_pdf
    
    def merge_esign_certificate(self, original_pdf: bytes, esign_pdf: bytes) -> bytes:
        return original_pdf

pdf_service = PDFService()
