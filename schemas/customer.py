# app/schemas/customer.py
"""
Ampalone Partner Portal - Customer Schemas
Version: 1.0.0
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CustomerType(str, Enum):
    PROSPECT = "prospect"
    LEAD = "lead"
    CUSTOMER = "customer"


class CustomerStatus(str, Enum):
    PROSPECT = "prospect"
    LEAD = "lead"
    CUSTOMER = "customer"
    INACTIVE = "inactive"


class CustomerBase(BaseModel):
    customer_type: CustomerType
    company_name: str = Field(..., min_length=2, max_length=255)
    industry: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[float] = None
    country_code: str = "IND"
    contact_person_name: str = Field(..., min_length=2, max_length=100)
    designation: Optional[str] = None
    email: EmailStr
    phone: str
    billing_address: str
    city: str
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: str = "India"
    data_processing_consent: bool = False
    gdpr_applicable: bool = False


class CustomerCreateRequest(CustomerBase):
    pan_number: Optional[str] = None
    gst_number: Optional[str] = None
    cin_number: Optional[str] = None
    tax_id: Optional[str] = None


class CustomerResponse(BaseModel):
    customer_id: int
    partner_id: int
    customer_type: str
    company_name: str
    industry: Optional[str]
    contact_person_name: str
    email: EmailStr
    phone: str
    status: CustomerStatus
    source: str
    created_at: datetime
    tagged_by: int
    
    model_config = ConfigDict(from_attributes=True)


class CustomerTagRequest(BaseModel):
    customer_id: int
    partner_id: int
    relationship_type: str = "referral"
    commission_rate: float = 25.0
    is_exclusive: bool = False
