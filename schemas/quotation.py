# app/schemas/quotation.py
"""
Ampalone Partner Portal - Quotation Schemas
Version: 1.0.0
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class QuotationStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CONVERTED = "converted"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class QuotationItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)
    discount_percentage: float = Field(default=0, ge=0, le=100)
    term_months: int = Field(default=12, ge=1, le=60)


class QuotationGenerateRequest(BaseModel):
    customer_id: int
    items: List[QuotationItemRequest]
    valid_days: int = Field(default=30, ge=1, le=90)
    notes: Optional[str] = None
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v: List[QuotationItemRequest]) -> List[QuotationItemRequest]:
        if not v or len(v) == 0:
            raise ValueError('At least one item is required')
        return v


class QuotationResponse(BaseModel):
    quotation_id: int
    quotation_number: str
    partner_id: int
    customer_id: int
    total_list_price: float
    discount_percentage: float
    discount_amount: float
    partner_margin: float
    final_price: float
    currency: str
    requires_approval: bool
    approval_status: ApprovalStatus
    valid_from: date
    valid_to: date
    status: QuotationStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class QuotationListResponse(BaseModel):
    quotations: List[QuotationResponse]
    total: int
    page: int
    page_size: int
