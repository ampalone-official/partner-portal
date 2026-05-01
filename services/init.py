# app/services/__init__.py
"""
Ampalone Partner Portal - Services Package
Version: 1.0.0
"""

from app.services.email_service import (
    EmailService,
    email_service,
    send_welcome_email,
    send_approval_email
)

__all__ = [
    "EmailService",
    "email_service",
    "send_welcome_email",
    "send_approval_email"
]
