# app/api/documents.py
"""
Ampalone Partner Portal - Document API Routes
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.partner import Partner
from app.utils.security import get_current_partner
import os

router = APIRouter()

DOCUMENT_PATHS = {
    'nda': 'documents/AMP-NDA-2026-V1.0.pdf',
    'msa': 'documents/AMP-MSA-2026-V1.0.pdf',
    'sla': 'documents/AMP-SLA-2026-V1.0.pdf'
}


@router.get("/{doc_type}")
async def download_document(
    doc_type: str,
    db: Session = Depends(get_db),
    current_partner: Partner = Depends(get_current_partner)
):
    """Download legal documents"""
    if doc_type not in DOCUMENT_PATHS:
        raise HTTPException(status_code=400, detail="Invalid document type")
    
    file_path = DOCUMENT_PATHS[doc_type]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    return FileResponse(
        path=file_path,
        filename=f"Ampalone-{doc_type.upper()}.pdf",
        media_type="application/pdf"
    )
