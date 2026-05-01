# app/api/customers.py
"""
Ampalone Partner Portal - Customer API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.customer import Customer
from app.models.partner import Partner
from app.models.document import PipelineTracking, PartnerCustomerMapping
from app.schemas.customer import CustomerCreateRequest
from app.utils.security import get_current_partner

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_customer(
    customer_data: CustomerCreateRequest,
    db: Session = Depends(get_db),
    current_partner: Partner = Depends(get_current_partner)
):
    """Register and tag customer (Partner)"""
    # Check if customer already exists
    existing_customer = db.query(Customer).filter(
        (Customer.email == customer_data.email.lower()) |
        ((Customer.company_name == customer_data.company_name) & 
         (Customer.country_code == customer_data.country_code))
    ).first()
    
    if existing_customer:
        existing_mapping = db.query(PartnerCustomerMapping).filter(
            PartnerCustomerMapping.customer_id == existing_customer.customer_id,
            PartnerCustomerMapping.partner_id == current_partner.partner_id
        ).first()
        
        if existing_mapping:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer already tagged by this partner"
            )
        
        mapping = PartnerCustomerMapping(
            partner_id=current_partner.partner_id,
            customer_id=existing_customer.customer_id,
            commission_rate=current_partner.margin_percentage,
            relationship_type="referral"
        )
        db.add(mapping)
        db.commit()
        
        return {
            "success": True,
            "message": "Existing customer tagged successfully",
            "data": {"customer_id": existing_customer.customer_id}
        }
    
    # Create new customer
    customer = Customer(
        partner_id=current_partner.partner_id,
        customer_type=customer_data.customer_type,
        company_name=customer_data.company_name,
        industry=customer_data.industry,
        company_size=customer_data.company_size,
        annual_revenue=customer_data.annual_revenue,
        country_code=customer_data.country_code,
        pan_number=customer_data.pan_number,
        gst_number=customer_data.gst_number,
        cin_number=customer_data.cin_number,
        tax_id=customer_data.tax_id,
        contact_person_name=customer_data.contact_person_name,
        designation=customer_data.designation,
        email=customer_data.email.lower(),
        phone=customer_data.phone,
        billing_address=customer_data.billing_address,
        city=customer_data.city,
        state=customer_data.state,
        pincode=customer_data.pincode,
        country=customer_data.country,
        data_processing_consent=customer_data.data_processing_consent,
        gdpr_applicable=customer_data.gdpr_applicable,
        status="prospect",
        source="partner_referral",
        tagged_by=current_partner.partner_id
    )
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    # Create mapping
    mapping = PartnerCustomerMapping(
        partner_id=current_partner.partner_id,
        customer_id=customer.customer_id,
        commission_rate=current_partner.margin_percentage,
        relationship_type="referral"
    )
    db.add(mapping)
    
    # Create pipeline entry
    pipeline = PipelineTracking(
        partner_id=current_partner.partner_id,
        customer_id=customer.customer_id,
        stage="prospect",
        probability_percentage=10,
        expected_value=0
    )
    db.add(pipeline)
    db.commit()
    
    return {
        "success": True,
        "message": "Customer registered and tagged successfully",
        "data": {
            "customer_id": customer.customer_id,
            "company_name": customer.company_name,
            "email": customer.email,
            "status": customer.status
        }
    }
