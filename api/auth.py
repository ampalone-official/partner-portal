# app/api/auth.py
"""
Ampalone Partner Portal - Authentication API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.partner import Partner, PartnerCredentials
from app.schemas.auth import Token
from app.utils.security import verify_password, create_access_token, create_refresh_token, decode_token, get_password_hash
from app.config import settings
from app.services.email_service import send_welcome_email
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_partner(request: Request, db: Session = Depends(get_db)):
    """Partner registration endpoint"""
    from app.schemas.partner import PartnerRegisterRequest
    from app.utils.validators import validate_pan, validate_gst
    
    body = await request.json()
    
    # Validate PAN/GST for Indian partners
    if body.get('country_code') == 'IND':
        if not validate_pan(body.get('pan_number')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid PAN number is required for Indian partners"
            )
        if not validate_gst(body.get('gst_number')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid GST number is required for Indian partners"
            )
    
    # Check if email already exists
    existing_partner = db.query(Partner).filter(Partner.email == body['email'].lower()).first()
    if existing_partner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create partner record
    partner = Partner(
        partner_type=body['partner_type'],
        company_name=body['company_name'],
        trading_name=body.get('trading_name'),
        pan_number=body.get('pan_number', '').upper(),
        gst_number=body.get('gst_number', '').upper(),
        cin_number=body.get('cin_number'),
        country_code=body.get('country_code', 'IND'),
        tax_id=body.get('tax_id'),
        authorized_person_name=body['authorized_person_name'],
        designation=body.get('designation'),
        email=body['email'].lower(),
        phone=body['phone'],
        alternate_phone=body.get('alternate_phone'),
        registered_address=body['registered_address'],
        city=body['city'],
        state=body['state'],
        pincode=body['pincode'],
        country=body.get('country', 'India'),
        bank_name=body.get('bank_name'),
        account_number=body.get('account_number'),
        ifsc_code=body.get('ifsc_code', '').upper(),
        account_holder_name=body.get('account_holder_name'),
        margin_percentage=settings.DEFAULT_PARTNER_MARGIN,
        status="pending_approval"
    )
    
    db.add(partner)
    db.commit()
    db.refresh(partner)
    
    # Create credentials
    credentials = PartnerCredentials(
        partner_id=partner.partner_id,
        password_hash=get_password_hash(body['password'])
    )
    db.add(credentials)
    db.commit()
    
    # Send welcome email
    try:
        await send_welcome_email(partner.email, partner.company_name)
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
    
    return {
        "success": True,
        "message": "Partner registration submitted successfully. Awaiting admin approval.",
        "data": {
            "partner_id": partner.partner_id,
            "company_name": partner.company_name,
            "email": partner.email,
            "status": partner.status,
            "created_at": partner.created_at.isoformat()
        }
    }


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Partner login endpoint"""
    partner = db.query(Partner).filter(Partner.email == form_data.username.lower()).first()
    
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    credentials = db.query(PartnerCredentials).filter(
        PartnerCredentials.partner_id == partner.partner_id
    ).first()
    
    if not credentials or not verify_password(form_data.password, credentials.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if partner.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Partner account is {partner.status}. Please contact support."
        )
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": partner.partner_id, "email": partner.email, "role": "partner"}
    )
    refresh_token = create_refresh_token(
        data={"sub": partner.partner_id, "email": partner.email}
    )
    
    # Update refresh token in database
    credentials.refresh_token = refresh_token
    credentials.last_login = datetime.utcnow()
    credentials.failed_login_attempts = 0
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me")
async def get_current_user(current_partner: Partner = Depends(get_current_partner)):
    """Get current authenticated partner details"""
    return {
        "success": True,
        "data": {
            "partner_id": current_partner.partner_id,
            "company_name": current_partner.company_name,
            "email": current_partner.email,
            "partner_tier": current_partner.partner_tier,
            "margin_percentage": current_partner.margin_percentage,
            "status": current_partner.status
        }
    }

