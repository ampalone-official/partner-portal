# app/api/__init__.py
"""
Ampalone Partner Portal - API Routes Package
Version: 1.0.0
"""

from app.api.auth import router as auth_router
from app.api.partners import router as partners_router
from app.api.customers import router as customers_router
from app.api.quotations import router as quotations_router
from app.api.approvals import router as approvals_router
from app.api.documents import router as documents_router
from app.api.analytics import router as analytics_router
from app.api.admin import router as admin_router

__all__ = [
    "auth_router",
    "partners_router",
    "customers_router",
    "quotations_router",
    "approvals_router",
    "documents_router",
    "analytics_router",
    "admin_router"
]
