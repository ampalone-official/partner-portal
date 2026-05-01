# app/models/approval.py
"""
Ampalone Partner Portal - Approval Workflow Model
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ApprovalRequest(Base):
    """Approval request model for discount approvals"""
    
    __tablename__ = "approval_requests"
    
    approval_id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), index=True)
    request_type = Column(String(50), default="discount_approval")
    requested_by = Column(Integer, ForeignKey("partners.partner_id"))
    current_discount = Column(Float, nullable=False)
    requested_discount = Column(Float, nullable=False)
    justification = Column(Text)
    status = Column(String(20), default="pending")
    reviewed_by = Column(Integer, ForeignKey("users.user_id"))
    reviewed_at = Column(DateTime(timezone=True))
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    quotation = relationship("Quotation", back_populates="approval_requests")
