# app/api/quotations.py
"""
Ampalone Partner Portal - Quotation API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.quotation import Quotation, QuotationItem
from app.models.partner import Partner
from app.models.customer import Customer
from app.models.document import PartnerCustomerMapping
from app.schemas.quotation import QuotationGenerateRequest
from app.utils.security import get_current_partner
from app.utils.pdf_generator import generate_quotation_pdf
from app.utils.csv_generator import generate_quotation_csv

router = APIRouter()


@router.post("/generate", response_model=dict, status_code=status.HTTP_201_CREATED)
async def generate_quotation(
    quotation_data: QuotationGenerateRequest,
    db: Session = Depends(get_db),
    current_partner: Partner = Depends(get_current_partner)
):
    """Generate quotation for customer"""
    from app.config import settings
    from app.utils.security import generate_quotation_number
    
    # Verify customer belongs to partner
    mapping = db.query(PartnerCustomerMapping).filter(
        PartnerCustomerMapping.partner_id == current_partner.partner_id,
        PartnerCustomerMapping.customer_id == quotation_data.customer_id
    ).first()
    
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only generate quotations for your tagged customers"
        )
    
    # Calculate pricing
    total_list_price = 0
    total_discount = 0
    max_discount = 0
    quotation_items = []
    
    for item in quotation_data.items:
        from app.models.product import Product
        product = db.query(Product).filter(Product.product_id == item.product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        discount = item.discount_percentage
        if discount > max_discount:
            max_discount = discount
        
        line_total = product.list_price * item.quantity * (1 - discount / 100)
        total_list_price += product.list_price * item.quantity
        total_discount += (product.list_price * item.quantity * discount / 100)
        
        quotation_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": product.list_price,
            "discount_percentage": discount,
            "line_total": line_total
        })
    
    # Check approval requirement
    requires_approval = max_discount > settings.MAX_DISCOUNT_WITHOUT_APPROVAL
    final_price = total_list_price - total_discount
    partner_margin = total_list_price * (current_partner.margin_percentage / 100)
    
    # Generate quotation number
    quotation_number = generate_quotation_number()
    
    # Create quotation
    from datetime import date, timedelta
    quotation = Quotation(
        quotation_number=quotation_number,
        partner_id=current_partner.partner_id,
        customer_id=quotation_data.customer_id,
        total_list_price=total_list_price,
        discount_percentage=max_discount,
        discount_amount=total_discount,
        partner_margin=partner_margin,
        final_price=final_price,
        requires_approval=requires_approval,
        approval_status="pending" if requires_approval else "approved",
        valid_from=date.today(),
        valid_to=date.today() + timedelta(days=quotation_data.valid_days),
        status="draft",
        documents_attached=True,
        nda_attached=True,
        master_agreement_attached=True,
        sla_attached=True,
        created_by=current_partner.partner_id
    )
    
    db.add(quotation)
    db.commit()
    db.refresh(quotation)
    
    # Create quotation items
    for qi in quotation_items:
        item = QuotationItem(
            quotation_id=quotation.quotation_id,
            product_id=qi["product_id"],
            quantity=qi["quantity"],
            unit_price=qi["unit_price"],
            discount_percentage=qi["discount_percentage"],
            line_total=qi["line_total"]
        )
        db.add(item)
    db.commit()
    
    response_message = (
        "Quotation created and sent for approval" 
        if requires_approval 
        else "Quotation generated successfully"
    )
    
    return {
        "success": True,
        "message": response_message,
        "data": {
            "quotation_id": quotation.quotation_id,
            "quotation_number": quotation.quotation_number,
            "requires_approval": requires_approval,
            "total_list_price": total_list_price,
            "discount_amount": total_discount,
            "final_price": final_price,
            "partner_margin": partner_margin
        }
    }


@router.get("/{quotation_id}/export/{format}")
async def export_quotation(
    quotation_id: int,
    format: str,
    db: Session = Depends(get_db),
    current_partner: Partner = Depends(get_current_partner)
):
    """Export quotation as PDF or CSV"""
    if format not in ['pdf', 'csv']:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'pdf' or 'csv'")
    
    quotation = db.query(Quotation).filter(
        Quotation.quotation_id == quotation_id,
        Quotation.partner_id == current_partner.partner_id
    ).first()
    
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    
    items = db.query(QuotationItem).filter(QuotationItem.quotation_id == quotation_id).all()
    customer = db.query(Customer).filter(Customer.customer_id == quotation.customer_id).first()
    
    if format == 'pdf':
        pdf_buffer = generate_quotation_pdf(quotation, items, customer, current_partner)
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Quotation-{quotation.quotation_number}.pdf"}
        )
    elif format == 'csv':
        csv_buffer = generate_quotation_csv(quotation, items)
        return Response(
            content=csv_buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=Quotation-{quotation.quotation_number}.csv"}
        )
