# app/models/customer.py
"""
Ampalone Partner Portal - Customer Model
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Customer(Base):
    """Customer/Prospect model for storing customer details"""
    
    __tablename__ = "customers"
    
    # Primary Key
    customer_id = Column(Integer, primary_key=True, index=True)
    
    # Partner Relationship
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), index=True)
    customer_type = Column(String(50), nullable=False)
    
    # Company Details
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    company_size = Column(String(50))
    annual_revenue = Column(Float)
    
    # Compliance
    country_code = Column(String(3), default="IND")
    pan_number = Column(String(10))
    gst_number = Column(String(15))
    cin_number = Column(String(21))
    tax_id = Column(String(50))
    
    # Primary Contact
    contact_person_name = Column(String(100), nullable=False)
    designation = Column(String(100))
    email = Column(String(150), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    
    # Business Address
    billing_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    pincode = Column(String(10))
    country = Column(String(100), default="India")
    
    # Data Processing Compliance
    data_processing_consent = Column(Boolean, default=False)
    gdpr_applicable = Column(Boolean, default=False)
    data_retention_period = Column(Integer, default=36)
    
    # Status
    status = Column(String(20), default="prospect")
    source = Column(String(50), default="partner_referral")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tagged_by = Column(Integer, ForeignKey("partners.partner_id"))
    
    # Relationships
    partner = relationship("Partner", back_populates="customers", foreign_keys=[partner_id])
    quotations = relationship("Quotation", back_populates="customer")
    pipeline = relationship("PipelineTracking", back_populates="customer", uselist=False)
    
    def __repr__(self):
        return f"<Customer {self.company_name} ({self.email})>"
