from jinja2 import Environment, FileSystemLoader, Template
from typing import Dict, Any
import os
from app.models.agreement import AgreementType

class TemplateService:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def get_template_fields(self, agreement_type: AgreementType) -> Dict[str, str]:
        field_mappings = {
            AgreementType.RENTAL: {
                "landlordName": "Landlord Full Name",
                "landlordAddress": "Landlord Address",
                "tenantName": "Tenant Full Name", 
                "tenantAddress": "Tenant Address",
                "propertyAddress": "Property Address",
                "rentAmount": "Monthly Rent Amount",
                "securityDeposit": "Security Deposit",
                "leaseDuration": "Lease Duration (months)",
                "startDate": "Lease Start Date",
                "endDate": "Lease End Date"
            },
            AgreementType.EMPLOYMENT: {
                "employerName": "Employer Company Name",
                "employerAddress": "Employer Address",
                "employeeName": "Employee Full Name",
                "employeeAddress": "Employee Address",
                "position": "Job Position",
                "salary": "Annual Salary",
                "startDate": "Employment Start Date",
                "probationPeriod": "Probation Period (months)",
                "workLocation": "Work Location"
            },
            AgreementType.SERVICE: {
                "serviceProviderName": "Service Provider Name",
                "serviceProviderAddress": "Service Provider Address",
                "clientName": "Client Name",
                "clientAddress": "Client Address",
                "serviceDescription": "Service Description",
                "serviceAmount": "Service Amount",
                "startDate": "Service Start Date",
                "endDate": "Service End Date",
                "paymentTerms": "Payment Terms"
            }
        }
        return field_mappings.get(agreement_type, {})
    
    def render_template(self, agreement_type: AgreementType, template_data: Dict[str, Any]) -> str:
        template_name = f"{agreement_type.value}.html"
        try:
            template = self.env.get_template(template_name)
            return template.render(**template_data)
        except Exception as e:
            return self._get_default_template(agreement_type, template_data)
    
    def _get_default_template(self, agreement_type: AgreementType, template_data: Dict[str, Any]) -> str:
        if agreement_type == AgreementType.RENTAL:
            return f"""
            <html>
            <head><title>Rental Agreement</title></head>
            <body>
                <h1>RENTAL AGREEMENT</h1>
                <p>This rental agreement is made between:</p>
                <p><strong>Landlord:</strong> {template_data.get('landlordName', '[Landlord Name]')}</p>
                <p><strong>Address:</strong> {template_data.get('landlordAddress', '[Landlord Address]')}</p>
                <p><strong>Tenant:</strong> {template_data.get('tenantName', '[Tenant Name]')}</p>
                <p><strong>Address:</strong> {template_data.get('tenantAddress', '[Tenant Address]')}</p>
                <p><strong>Property:</strong> {template_data.get('propertyAddress', '[Property Address]')}</p>
                <p><strong>Monthly Rent:</strong> ₹{template_data.get('rentAmount', '[Rent Amount]')}</p>
                <p><strong>Security Deposit:</strong> ₹{template_data.get('securityDeposit', '[Security Deposit]')}</p>
                <p><strong>Lease Period:</strong> {template_data.get('startDate', '[Start Date]')} to {template_data.get('endDate', '[End Date]')}</p>
            </body>
            </html>
            """
        elif agreement_type == AgreementType.EMPLOYMENT:
            return f"""
            <html>
            <head><title>Employment Agreement</title></head>
            <body>
                <h1>EMPLOYMENT AGREEMENT</h1>
                <p>This employment agreement is made between:</p>
                <p><strong>Employer:</strong> {template_data.get('employerName', '[Employer Name]')}</p>
                <p><strong>Employee:</strong> {template_data.get('employeeName', '[Employee Name]')}</p>
                <p><strong>Position:</strong> {template_data.get('position', '[Position]')}</p>
                <p><strong>Salary:</strong> ₹{template_data.get('salary', '[Salary]')} per annum</p>
                <p><strong>Start Date:</strong> {template_data.get('startDate', '[Start Date]')}</p>
                <p><strong>Work Location:</strong> {template_data.get('workLocation', '[Work Location]')}</p>
            </body>
            </html>
            """
        else:
            return f"""
            <html>
            <head><title>Service Agreement</title></head>
            <body>
                <h1>SERVICE AGREEMENT</h1>
                <p>This service agreement is made between:</p>
                <p><strong>Service Provider:</strong> {template_data.get('serviceProviderName', '[Service Provider]')}</p>
                <p><strong>Client:</strong> {template_data.get('clientName', '[Client Name]')}</p>
                <p><strong>Service:</strong> {template_data.get('serviceDescription', '[Service Description]')}</p>
                <p><strong>Amount:</strong> ₹{template_data.get('serviceAmount', '[Service Amount]')}</p>
                <p><strong>Duration:</strong> {template_data.get('startDate', '[Start Date]')} to {template_data.get('endDate', '[End Date]')}</p>
            </body>
            </html>
            """

template_service = TemplateService()
