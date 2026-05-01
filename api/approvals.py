# app/api/approvals.py
"""
Ampalone Partner Portal - Approval API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.partner import Partner
from app.models.approval import ApprovalRequest
from app.utils.security import get_current_partner

router = APIRouter()


@router.get("/", response_model=dict)
async def list_approvals(
    db: Session = Depends(get_db),
    current_partner: Partner = Depends(get_current_partner)
):
    """List approval requests"""
    if current_partner.email.endswith("@ampalone.com"):
        # Admin sees all
        approvals = db.query(ApprovalRequest).order_by(ApprovalRequest.created_at.desc()).all()
    else:
        # Partner sees their own
        approvals = db.query(ApprovalRequest).filter(
            ApprovalRequest.requested_by == current_partner.partner_id
        ).order_by(ApprovalRequest.created_at.desc()).all()
    
    return {
        "success": True,
        "data": {
            "approvals": approvals,
            "total": len(approvals)
        }
    }
