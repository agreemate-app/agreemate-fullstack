from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import UserCreate, UserLogin, User, Token
from app.services.auth_service import auth_service
from app.core.security import verify_token

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=User)
async def register(user_create: UserCreate):
    return auth_service.register_user(user_create)

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    return auth_service.authenticate_user(user_login)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = auth_service.get_current_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
