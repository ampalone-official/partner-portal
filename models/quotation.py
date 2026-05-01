# app/models/quotation.py
"""
Ampalone Partner Portal - Quotation Model
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import date

class Quotation(Base):
    """Quotation model for storing quotation details"""
    
    __tablename__ = "quotations"
    
    # Primary Key
    quotation_id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String(50), unique=True, nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), index=True)
    
    # Pricing
    total_list_price = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    partner_margin = Column(Float, default=0)
    final_price = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    
    # Approval
    requires_approval = Column(Boolean, default=False)
    approval_status = Column(String(20), default="pending")
    approved_by = Column(Integer, ForeignKey("users.user_id"))
    approved_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    
    # Validity
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)
    
    # Status
    status = Column(String(20), default="draft")
    
    # Documents
    documents_attached = Column(Boolean, default=False)
    nda_attached = Column(Boolean, default=False)
    master_agreement_attached = Column(Boolean, default=False)
    sla_attached = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"))
    
    # Relationships
    partner = relationship("Partner", back_populates="quotations")
    customer = relationship("Customer", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")
    approval_requests = relationship("ApprovalRequest", back_populates="quotation")
    
    def __repr__(self):
        return f"<Quotation {self.quotation_number}>"
    
    @property
    def is_expired(self) -> bool:
        return date.today() > self.valid_to


class QuotationItem(Base):
    """Quotation line items"""
    
    __tablename__ = "quotation_items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0)
    line_total = Column(Float, nullable=False)
    pricing_model = Column(String(50))
    term_months = Column(Integer, default=12)
    
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product", back_populates="quotation_items")
