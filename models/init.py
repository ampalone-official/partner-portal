# app/models/__init__.py
"""
Ampalone Partner Portal - Models Package
Version: 1.0.0
"""

from app.database import Base
from app.models.partner import Partner, PartnerCredentials
from app.models.customer import Customer
from app.models.product import Product, PricingConfig
from app.models.quotation import Quotation, QuotationItem
from app.models.approval import ApprovalRequest
from app.models.document import Document, PipelineTracking, PartnerCustomerMapping, AuditLog

# Export all models
__all__ = [
    "Base",
    "Partner",
    "PartnerCredentials",
    "Customer",
    "Product",
    "PricingConfig",
    "Quotation",
    "QuotationItem",
    "ApprovalRequest",
    "Document",
    "PipelineTracking",
    "PartnerCustomerMapping",
    "AuditLog"
]

