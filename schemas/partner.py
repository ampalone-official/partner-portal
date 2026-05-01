# app/schemas/partner.py
"""
Ampalone Partner Portal - Partner Schemas (Pydantic)
Version: 1.0.0
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
import re


class PartnerType(str, Enum):
    INDIVIDUAL = "Individual"
    LLP = "LLP"
    PRIVATE_LTD = "Private Ltd"
    PUBLIC_LTD = "Public Ltd"
    CORPORATION = "Corporation"


class PartnerStatus(str, Enum):
    PENDING = "pending_approval"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class PartnerTier(str, Enum):
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class PartnerBase(BaseModel):
    partner_type: PartnerType
    company_name: str = Field(..., min_length=2, max_length=255)
    trading_name: Optional[str] = None
    country_code: str = Field(default="IND", max_length=3)
    authorized_person_name: str = Field(..., min_length=2, max_length=100)
    designation: Optional[str] = None
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    alternate_phone: Optional[str] = None
    registered_address: str
    city: str
    state: str
    pincode: str
    country: str = "India"


class PartnerIndiaCompliance(BaseModel):
    pan_number: str
    gst_number: str
    cin_number: Optional[str] = None
    llp_number: Optional[str] = None
    
    @field_validator('pan_number')
    @classmethod
    def validate_pan(cls, v: str) -> str:
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        if not re.match(pan_pattern, v.upper()):
            raise ValueError('Invalid PAN format. Expected: ABCDE1234F')
        return v.upper()
    
    @field_validator('gst_number')
    @classmethod
    def validate_gst(cls, v: str) -> str:
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        if not re.match(gst_pattern, v.upper()):
            raise ValueError('Invalid GST format')
        return v.upper()


class PartnerInternationalCompliance(BaseModel):
    tax_id: str
    vat_number: Optional[str] = None


class PartnerBankingDetails(BaseModel):
    bank_name: str
    account_number: str = Field(..., min_length=5, max_length=50)
    ifsc_code: Optional[str] = Field(None, max_length=11)
    account_holder_name: str
    bank_address: Optional[str] = None


class PartnerRegisterRequest(PartnerBase, PartnerIndiaCompliance, PartnerBankingDetails):
    password: str = Field(..., min_length=8)
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class PartnerResponse(BaseModel):
    partner_id: int
    partner_type: str
    company_name: str
    trading_name: Optional[str]
    email: EmailStr
    phone: str
    status: PartnerStatus
    partner_tier: PartnerTier
    margin_percentage: float
    agreement_signed: bool
    nda_signed: bool
    country_code: str
    created_at: datetime
    approved_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PartnerListResponse(BaseModel):
    partners: List[PartnerResponse]
    total: int
    page: int
    page_size: int


class PartnerUpdateRequest(BaseModel):
    trading_name: Optional[str] = None
    designation: Optional[str] = None
    alternate_phone: Optional[str] = None
    registered_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    account_holder_name: Optional[str] = None
