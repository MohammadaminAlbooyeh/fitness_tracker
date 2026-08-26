"""Security utilities for JWT, password hashing, and request authentication."""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from shared_lib.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 bearer scheme used to protect endpoints. tokenUrl points at the
# user-service login endpoint so the OpenAPI docs can be used to obtain a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT, raising 401 on any failure."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise credentials_exception from exc
    return payload


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """Dependency that enforces authentication on a protected endpoint.

    Returns the decoded JWT payload (including the ``sub`` claim identifying the
    authenticated user). Raises 401 when the token is missing or invalid.
    """
    payload = decode_token(token)
    if payload.get("sub") is None:
        raise credentials_exception
    return payload
