# app/models/document.py
"""
Ampalone Partner Portal - Document & Audit Models
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Document(Base):
    """Document management model"""
    
    __tablename__ = "documents"
    
    document_id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String(50), nullable=False)
    document_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(10), default="pdf")
    version = Column(String(20), default="1.0")
    effective_date = Column(Date)
    expiry_date = Column(Date)
    is_active = Column(Boolean, default=True)
    uploaded_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PipelineTracking(Base):
    """Pipeline tracking for sales funnel"""
    
    __tablename__ = "pipeline_tracking"
    
    tracking_id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), index=True)
    stage = Column(String(50), nullable=False)
    probability_percentage = Column(Integer, default=0)
    expected_value = Column(Float)
    expected_close_date = Column(Date)
    actual_close_date = Column(Date)
    loss_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    customer = relationship("Customer", back_populates="pipeline")


class PartnerCustomerMapping(Base):
    """Partner-Customer relationship mapping"""
    
    __tablename__ = "partner_customer_mapping"
    
    mapping_id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    relationship_type = Column(String(50), default="referral")
    commission_rate = Column(Float, default=25.00)
    is_exclusive = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        # Ensure unique partner-customer mapping
        sqlalchemy.UniqueConstraint('partner_id', 'customer_id', name='unique_partner_customer'),
    )


class AuditLog(Base):
    """Audit log for tracking all actions"""
    
    __tablename__ = "audit_log"
    
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_type = Column(String(20))
    action = Column(String(100), nullable=False)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    ip_address = Column(String(45))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
