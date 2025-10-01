from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings
from app.core.professional_auth import get_current_professional
from app.db.session import SessionLocal

security = HTTPBearer()

async def professional_middleware(request: Request, credentials: HTTPAuthorizationCredentials = security):
    """Middleware to handle professional authentication."""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        if payload.get("type") != "professional":
            raise HTTPException(status_code=403, detail="Not a professional account")
            
        db = SessionLocal()
        try:
            professional = await get_current_professional(db, token)
            request.state.professional = professional
        finally:
            db.close()
            
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))