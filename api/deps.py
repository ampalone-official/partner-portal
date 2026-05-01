# app/api/deps.py
"""
Ampalone Partner Portal - API Dependencies
Version: 1.0.0
"""

from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_partner, get_current_admin

__all__ = [
    "get_db",
    "get_current_partner",
    "get_current_admin"
]
