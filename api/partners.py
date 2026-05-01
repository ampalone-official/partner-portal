# app/api/partners.py
"""
Ampalone Partner Portal - Partner API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.partner import Partner
from app.utils.security import get_current_partner, get_current_admin

router = APIRouter()


@router.get("/", response_model=dict)
async def list_partners(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    partner_tier: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Partner = Depends(get_current_admin)
):
    """List all partners (Admin only)"""
    query = db.query(Partner)
    
    if status:
        query = query.filter(Partner.status == status)
    if partner_tier:
        query = query.filter(Partner.partner_tier == partner_tier)
    
    total = query.count()
    partners = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": {
            "partners": partners,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    }


@router.get("/{partner_id}", response_model=dict)
async def get_partner(
    partner_id: int,
    db: Session = Depends(get_db),
    current_user: Partner = Depends(get_current_partner)
):
    """Get partner details"""
    if current_user.partner_id != partner_id and current_user.partner_tier != "platinum":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this partner's details"
        )
    
    partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner not found"
        )
    
    return {"success": True, "data": partner}


@router.post("/{partner_id}/approve", response_model=dict)
async def approve_partner(
    partner_id: int,
    db: Session = Depends(get_db),
    current_user: Partner = Depends(get_current_admin)
):
    """Approve partner registration (Admin only)"""
    partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    if partner.status == "active":
        raise HTTPException(status_code=400, detail="Partner is already approved")
    
    partner.status = "active"
    partner.approved_at = datetime.utcnow()
    partner.approved_by = current_user.partner_id
    db.commit()
    
    return {"success": True, "message": "Partner approved successfully"}
