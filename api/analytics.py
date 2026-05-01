# app/api/analytics.py
"""
Ampalone Partner Portal - Analytics API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.database import get_db
from app.models.quotation import Quotation
from app.models.customer import Customer
from app.models.document import PipelineTracking
from app.models.partner import Partner
from app.models.quotation import QuotationItem
from app.models.product import Product
from app.utils.security import get_current_partner

router = APIRouter()


@router.get("/dashboard", response_model=dict)
async def get_analytics_dashboard(
    db: Session = Depends(get_db),
    current_partner: Partner = Depends(get_current_partner)
):
    """Get analytics dashboard data"""
    role = "admin" if current_partner.email.endswith("@ampalone.com") else "partner"
    
    # Pipeline Analytics
    pipeline_query = db.query(
        PipelineTracking.stage,
        func.count(PipelineTracking.tracking_id).label('count'),
        func.sum(PipelineTracking.expected_value).label('total_value')
    )
    
    if role != "admin":
        pipeline_query = pipeline_query.filter(PipelineTracking.partner_id == current_partner.partner_id)
    
    pipeline = pipeline_query.group_by(PipelineTracking.stage).all()
    
    # Quotation Status
    quotation_status_query = db.query(
        Quotation.status,
        func.count(Quotation.quotation_id).label('count'),
        func.sum(Quotation.final_price).label('total_value')
    )
    
    if role != "admin":
        quotation_status_query = quotation_status_query.filter(Quotation.partner_id == current_partner.partner_id)
    
    quotation_status = quotation_status_query.group_by(Quotation.status).all()
    
    # Monthly Trends
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    trends_query = db.query(
        extract('year', Quotation.created_at).label('year'),
        extract('month', Quotation.created_at).label('month'),
        func.count(Quotation.quotation_id).label('quotations_count'),
        func.sum(Quotation.final_price).label('total_value')
    ).filter(Quotation.created_at >= twelve_months_ago)
    
    if role != "admin":
        trends_query = trends_query.filter(Quotation.partner_id == current_partner.partner_id)
    
    trends = trends_query.group_by(
        extract('year', Quotation.created_at),
        extract('month', Quotation.created_at)
    ).order_by(
        extract('year', Quotation.created_at).desc(),
        extract('month', Quotation.created_at).desc()
    ).limit(12).all()
    
    return {
        "success": True,
        "data": {
            "pipeline": [
                {"stage": p.stage, "count": p.count, "total_value": float(p.total_value or 0)}
                for p in pipeline
            ],
            "quotation_status": [
                {"status": q.status, "count": q.count, "total_value": float(q.total_value or 0)}
                for q in quotation_status
            ],
            "monthly_trends": [
                {
                    "month": f"{int(t.year)}-{int(t.month):02d}",
                    "quotations_count": t.quotations_count,
                    "total_value": float(t.total_value or 0)
                }
                for t in trends
            ],
            "generated_at": datetime.utcnow().isoformat()
        }
    }
