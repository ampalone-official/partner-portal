# app/api/admin.py
"""
Ampalone Partner Portal - Admin API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.partner import Partner
from app.models.product import Product, PricingConfig
from app.utils.security import get_current_admin

router = APIRouter()


@router.post("/pricing", response_model=dict)
async def update_pricing(
    pricing_data: dict,
    db: Session = Depends(get_db),
    current_user: Partner = Depends(get_current_admin)
):
    """Update product pricing (Admin only)"""
    product_id = pricing_data.get('product_id')
    list_price = pricing_data.get('list_price')
    
    if not product_id or not list_price:
        raise HTTPException(status_code=400, detail="product_id and list_price required")
    
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Calculate partner price (25% margin)
    partner_price = list_price * 0.75
    
    # Update product
    product.list_price = list_price
    
    # Create pricing config
    from datetime import date
    pricing = PricingConfig(
        product_id=product_id,
        list_price=list_price,
        partner_price=partner_price,
        effective_from=date.today(),
        created_by=current_user.partner_id
    )
    db.add(pricing)
    db.commit()
    
    return {
        "success": True,
        "message": "Pricing updated successfully",
        "data": {
            "product_id": product_id,
            "list_price": list_price,
            "partner_price": partner_price
        }
    }


@router.post("/approvals/{approval_id}/{action}", response_model=dict)
async def handle_approval(
    approval_id: int,
    action: str,
    db: Session = Depends(get_db),
    current_user: Partner = Depends(get_current_admin)
):
    """Handle approval request (Admin only)"""
    if action not in ['approve', 'reject']:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    from app.models.approval import ApprovalRequest
    from datetime import datetime
    
    approval = db.query(ApprovalRequest).filter(ApprovalRequest.approval_id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    approval.status = "approved" if action == "approve" else "rejected"
    approval.reviewed_by = current_user.partner_id
    approval.reviewed_at = datetime.utcnow()
    
    # Update quotation
    from app.models.quotation import Quotation
    quotation = db.query(Quotation).filter(Quotation.quotation_id == approval.quotation_id).first()
    if quotation:
        quotation.approval_status = approval.status
        if action == "approve":
            quotation.status = "sent"
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Quotation {action}ed successfully"
    }
