from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from app.models.user import UserCreate, UserLogin, User, UserInDB, Token
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.database import db

class AuthService:
    @staticmethod
    def register_user(user_create: UserCreate) -> User:
        try:
            user_in_db = db.create_user(user_create)
            return User(**user_in_db.dict())
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    @staticmethod
    def authenticate_user(user_login: UserLogin) -> Token:
        user = db.get_user_by_email(user_login.email)
        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    @staticmethod
    def get_current_user(email: str) -> Optional[User]:
        user = db.get_user_by_email(email)
        if user:
            return User(**user.dict())
        return None

auth_service = AuthService()
