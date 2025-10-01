from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.professional import Professional, ProfessionalStatus
from app.models.users import User, UserRole
from app.db.session import SessionLocal
from app.schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_professional_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_professional_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_professional(
    db: Session,
    token: str = Depends(oauth2_scheme)
) -> Professional:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user or user.role != UserRole.PROFESSIONAL:
        raise credentials_exception
        
    professional = db.query(Professional).filter(
        Professional.user_id == user.id
    ).first()
    if not professional:
        raise credentials_exception
        
    return professional

async def get_current_active_professional(
    current_professional: Professional = Depends(get_current_professional),
) -> Professional:
    if current_professional.status != ProfessionalStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Professional account is not active"
        )
    return current_professional

def verify_professional_permissions(professional: Professional, required_permissions: list):
    """Verify that a professional has the required permissions."""
    if not professional.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Professional account is not verified"
        )
    
    # Add more permission checks as needed
    return True

def create_professional_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT token for professional access."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "professional"
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def authenticate_professional(
    db: Session,
    email: str,
    password: str
) -> Optional[Professional]:
    """Authenticate a professional user."""
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != UserRole.PROFESSIONAL:
        return None
        
    if not verify_professional_password(password, user.hashed_password):
        return None
        
    professional = db.query(Professional).filter(
        Professional.user_id == user.id
    ).first()
    if not professional:
        return None
        
    return professional