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
                "landlordPhone": "Landlord Phone Number",
                "landlordEmail": "Landlord Email",
                "tenantName": "Tenant Full Name", 
                "tenantAddress": "Tenant Address",
                "tenantPhone": "Tenant Phone Number",
                "tenantEmail": "Tenant Email",
                "propertyAddress": "Property Address",
                "propertyType": "Property Type",
                "rentAmount": "Monthly Rent Amount (₹)",
                "securityDeposit": "Security Deposit (₹)",
                "startDate": "Lease Start Date",
                "endDate": "Lease End Date",
                "lockInPeriod": "Lock-in Period (months)",
                "rentDueDate": "Rent Due Date (day of month)",
                "noticePeriod": "Notice Period (days)",
                "witness1Name": "Witness 1 Name",
                "witness1Address": "Witness 1 Address",
                "witness2Name": "Witness 2 Name",
                "witness2Address": "Witness 2 Address"
            },
            AgreementType.EMPLOYMENT: {
                "employerName": "Employer Company Name",
                "employerAddress": "Employer Address",
                "employerRegistration": "Company Registration Number",
                "employeeName": "Employee Full Name",
                "employeeAddress": "Employee Address",
                "employeePhone": "Employee Phone Number",
                "employeeEmail": "Employee Email",
                "employeePAN": "Employee PAN Number",
                "position": "Job Position",
                "department": "Department",
                "salary": "Annual Salary (₹)",
                "basicSalary": "Basic Salary (₹)",
                "allowances": "Allowances (₹)",
                "bonusStructure": "Bonus Structure",
                "startDate": "Employment Start Date",
                "contractDate": "Contract Date",
                "employmentType": "Employment Type",
                "probationPeriod": "Probation Period (months)",
                "workLocation": "Work Location",
                "reportingManager": "Reporting Manager",
                "workingHours": "Working Hours",
                "leaveEntitlement": "Annual Leave Days",
                "medicalInsurance": "Medical Insurance Details",
                "noticePeriod": "Notice Period (days)",
                "witness1Name": "Witness 1 Name",
                "witness1Address": "Witness 1 Address",
                "witness2Name": "Witness 2 Name",
                "witness2Address": "Witness 2 Address"
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
            },
            AgreementType.BUYER_SELLER: {
                "sellerName": "Seller Full Name",
                "sellerAddress": "Seller Address",
                "sellerPhone": "Seller Phone Number",
                "sellerEmail": "Seller Email",
                "buyerName": "Buyer Full Name",
                "buyerAddress": "Buyer Address", 
                "buyerPhone": "Buyer Phone Number",
                "buyerEmail": "Buyer Email",
                "propertyDescription": "Property Description",
                "propertyAddress": "Property Address",
                "salePrice": "Sale Price (₹)",
                "advanceAmount": "Advance Amount (₹)",
                "balanceAmount": "Balance Amount (₹)",
                "completionDate": "Completion Date",
                "agreementDate": "Agreement Date",
                "witness1Name": "Witness 1 Name",
                "witness1Address": "Witness 1 Address",
                "witness2Name": "Witness 2 Name",
                "witness2Address": "Witness 2 Address"
            },
            AgreementType.NDA: {
                "disclosingPartyName": "Disclosing Party Name",
                "disclosingPartyAddress": "Disclosing Party Address",
                "disclosingPartyEmail": "Disclosing Party Email",
                "receivingPartyName": "Receiving Party Name",
                "receivingPartyAddress": "Receiving Party Address",
                "receivingPartyEmail": "Receiving Party Email",
                "purpose": "Purpose of Disclosure",
                "termDuration": "Agreement Duration",
                "agreementDate": "Agreement Date"
            },
            AgreementType.LOAN: {
                "lenderName": "Lender Full Name",
                "lenderAddress": "Lender Address",
                "borrowerName": "Borrower Full Name",
                "borrowerAddress": "Borrower Address",
                "loanAmount": "Loan Amount (₹)",
                "interestRate": "Interest Rate (%)",
                "startDate": "Loan Start Date",
                "endDate": "Loan End Date",
                "repaymentDay": "Monthly Repayment Day",
                "lateInterestRate": "Late Payment Interest Rate (%)",
                "defaultInterestRate": "Default Interest Rate (%)",
                "agreementDate": "Agreement Date",
                "witness1Name": "Witness 1 Name",
                "witness1Address": "Witness 1 Address",
                "witness2Name": "Witness 2 Name",
                "witness2Address": "Witness 2 Address"
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
