from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
from app.models.user import User, UserInDB, UserCreate
from app.models.agreement import Agreement, AgreementCreate, AgreementUpdate, DocumentStatus
from app.core.security import get_password_hash

class InMemoryDatabase:
    def __init__(self):
        self.users: Dict[str, UserInDB] = {}
        self.agreements: Dict[str, Agreement] = {}
        self.user_emails: Dict[str, str] = {}
    
    def create_user(self, user_create: UserCreate) -> UserInDB:
        if user_create.email in self.user_emails:
            raise ValueError("Email already registered")
        
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_create.password)
        
        user_in_db = UserInDB(
            id=user_id,
            email=user_create.email,
            phone=user_create.phone,
            full_name=user_create.full_name,
            role=user_create.role,
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.users[user_id] = user_in_db
        self.user_emails[user_create.email] = user_id
        return user_in_db
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user_id = self.user_emails.get(email)
        if user_id:
            return self.users.get(user_id)
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        return self.users.get(user_id)
    
    def create_agreement(self, user_id: str, agreement_create: AgreementCreate) -> Agreement:
        agreement_id = str(uuid.uuid4())
        
        agreement = Agreement(
            id=agreement_id,
            user_id=user_id,
            title=agreement_create.title,
            agreement_type=agreement_create.agreement_type,
            template_data=agreement_create.template_data,
            parties=agreement_create.parties,
            state=agreement_create.state,
            stamp_duty_amount=agreement_create.stamp_duty_amount,
            status=DocumentStatus.DRAFT,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            activity_log=[{
                "action": "created",
                "timestamp": datetime.utcnow().isoformat(),
                "status": DocumentStatus.DRAFT
            }]
        )
        
        self.agreements[agreement_id] = agreement
        return agreement
    
    def get_agreement(self, agreement_id: str) -> Optional[Agreement]:
        return self.agreements.get(agreement_id)
    
    def update_agreement(self, agreement_id: str, agreement_update: AgreementUpdate) -> Optional[Agreement]:
        agreement = self.agreements.get(agreement_id)
        if not agreement:
            return None
        
        update_data = agreement_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agreement, field, value)
        
        agreement.updated_at = datetime.utcnow()
        agreement.activity_log.append({
            "action": "updated",
            "timestamp": datetime.utcnow().isoformat(),
            "changes": update_data
        })
        
        return agreement
    
    def update_agreement_status(self, agreement_id: str, status: DocumentStatus, additional_data: Optional[Dict[str, Any]] = None) -> Optional[Agreement]:
        agreement = self.agreements.get(agreement_id)
        if not agreement:
            return None
        
        old_status = agreement.status
        agreement.status = status
        agreement.updated_at = datetime.utcnow()
        
        log_entry: Dict[str, Any] = {
            "action": "status_changed",
            "timestamp": datetime.utcnow().isoformat(),
            "old_status": old_status.value,
            "new_status": status.value
        }
        
        if additional_data:
            log_entry.update(additional_data)
        
        agreement.activity_log.append(log_entry)
        return agreement
    
    def get_user_agreements(self, user_id: str) -> List[Agreement]:
        return [agreement for agreement in self.agreements.values() if agreement.user_id == user_id]

db = InMemoryDatabase()
