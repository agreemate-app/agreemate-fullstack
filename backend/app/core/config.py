from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-in-production-agreemate-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    LEEGALITY_AUTH_TOKEN: Optional[str] = None
    LEEGALITY_BASE_URL: str = "https://sandbox.leegality.com/api/v2.1"
    LEEGALITY_ENABLED: bool = False
    ESTAMP_API_KEY: Optional[str] = None
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    
    UPLOAD_DIR: str = "/tmp/agreemate_uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    
    class Config:
        env_file = ".env"

settings = Settings()
