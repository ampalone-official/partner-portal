# app/config.py
"""
Ampalone Partner Portal - Configuration Settings
Version: 1.0.0
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Ampalone Partner Portal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = [
        "https://www.ampalone.com",
        "https://portal.ampalone.com",
        "http://localhost:3000",
        "http://localhost:8080"
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ampalone_portal"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Security
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_MIN_LENGTH: int = 8
    
    # Partner Program
    DEFAULT_PARTNER_MARGIN: float = 25.0
    MAX_DISCOUNT_WITHOUT_APPROVAL: float = 60.0
    MIN_COMMISSION_PAYOUT: float = 25000.0  # INR
    COMMISSION_PAYOUT_DAYS: int = 30
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_DOCUMENT_TYPES: List[str] = [".pdf", ".doc", ".docx"]
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@ampalone.com"
    EMAIL_SUPPORT: str = "support@ampalone.com"
    EMAIL_LEGAL: str = "legal@ampalone.com"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Compliance
    COMPANY_CIN: str = "U72200KA2020PTC134567"
    COMPANY_GST: str = "29AAAAA0000A1Z5"
    COMPANY_ADDRESS: str = "Bangalore, Karnataka, India"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
