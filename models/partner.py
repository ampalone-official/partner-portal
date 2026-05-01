# app/models/partner.py
"""
Ampalone Partner Portal - Partner Model
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Partner(Base):
    """Partner model for storing partner registration details"""
    
    __tablename__ = "partners"
    
    # Primary Key
    partner_id = Column(Integer, primary_key=True, index=True)
    
    # Partner Type
    partner_type = Column(String(50), nullable=False)
    company_name = Column(String(255), nullable=False)
    trading_name = Column(String(255))
    
    # India Specific Compliance
    pan_number = Column(String(10))
    gst_number = Column(String(15))
    cin_number = Column(String(21))
    llp_number = Column(String(17))
    
    # International Compliance
    country_code = Column(String(3), default="IND")
    tax_id = Column(String(50))
    vat_number = Column(String(50))
    
    # Authorized Signatory
    authorized_person_name = Column(String(100), nullable=False)
    designation = Column(String(100))
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    alternate_phone = Column(String(20))
    
    # Business Address
    registered_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10))
    country = Column(String(100), default="India")
    
    # Banking Details
    bank_name = Column(String(100))
    account_number = Column(String(50))
    ifsc_code = Column(String(11))
    account_holder_name = Column(String(100))
    bank_address = Column(Text)
    
    # Partner Status & Terms
    status = Column(String(20), default="pending_approval")
    partner_tier = Column(String(20), default="silver")
    margin_percentage = Column(Float, default=25.00)
    agreement_signed = Column(Boolean, default=False)
    nda_signed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))
    approved_by = Column(Integer, ForeignKey("users.user_id"))
    
    # Relationships
    customers = relationship("Customer", back_populates="partner")
    quotations = relationship("Quotation", back_populates="partner")
    credentials = relationship("PartnerCredentials", back_populates="partner", uselist=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "pan_number ~ '^[A-Z]{5}[0-9]{4}[A-Z]{1}$' OR pan_number IS NULL",
            name="check_pan_format"
        ),
        CheckConstraint(
            "gst_number ~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$' OR gst_number IS NULL",
            name="check_gst_format"
        ),
    )
    
    def __repr__(self):
        return f"<Partner {self.company_name} ({self.email})>"
    
    @property
    def is_active(self) -> bool:
        return self.status == "active"
    
    @property
    def is_approved(self) -> bool:
        return self.approved_at is not None


class PartnerCredentials(Base):
    """Partner login credentials"""
    
    __tablename__ = "partner_credentials"
    
    credential_id = Column(Integer, primary_key=True)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), unique=True)
    password_hash = Column(String(255), nullable=False)
    refresh_token = Column(String(500))
    last_login = Column(DateTime(timezone=True))
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    
    partner = relationship("Partner", back_populates="credentials")
