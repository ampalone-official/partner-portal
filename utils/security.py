# app/utils/security.py
"""
Ampalone Partner Portal - Security Utilities
Version: 1.0.0
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.partner import Partner, PartnerCredentials
from app.schemas.auth import TokenData
import secrets

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            return None
        
        return TokenData(user_id=user_id, email=email, role=role)
    except JWTError:
        return None


async def get_current_partner(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Partner:
    """Get current authenticated partner"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    partner = db.query(Partner).filter(Partner.partner_id == payload.user_id).first()
    if partner is None:
        raise credentials_exception
    
    if partner.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Partner account is not active"
        )
    
    return partner


async def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Partner:
    """Get current authenticated admin"""
    partner = await get_current_partner(token, db)
    
    if partner.partner_tier != "platinum" and not partner.email.endswith("@ampalone.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return partner


def generate_quotation_number() -> str:
    """Generate unique quotation number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_str = secrets.token_hex(3).upper()
    return f"AMP-Q-{timestamp}-{random_str}"


def generate_document_id(doc_type: str, partner_id: int) -> str:
    """Generate unique document ID"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"AMP-{doc_type.upper()}-{partner_id}-{timestamp}"
