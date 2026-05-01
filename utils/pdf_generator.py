# app/utils/pdf_generator.py
"""
Ampalone Partner Portal - PDF Generation Utilities
Version: 1.0.0
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from io import BytesIO
from datetime import datetime
from typing import List


def generate_quotation_pdf(quotation, items: list, customer, partner) -> BytesIO:
    """
    Generate quotation PDF document
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    # Header
    elements.append(Paragraph("AMPALONE SOFTWARES", title_style))
    elements.append(Paragraph("AI-Powered Enterprise Security", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Quotation details
    elements.append(Paragraph("QUOTATION", styles['Heading2']))
    
    quotation_info = [
        ['Quotation Number:', quotation.quotation_number],
        ['Date:', quotation.created_at.strftime('%d %B %Y')],
        ['Valid Until:', quotation.valid_to.strftime('%d %B %Y')],
    ]
    
    quotation_table = Table(quotation_info, colWidths=[2*inch, 3*inch])
    quotation_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(quotation_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Customer details
    elements.append(Paragraph("Bill To:", styles['Heading3']))
    customer_info = [
        [customer.company_name],
        [f"Attn: {customer.contact_person_name}"],
        [customer.billing_address],
        [f"{customer.city}, {customer.state} {customer.pincode}"],
        [customer.country],
        [f"Email: {customer.email}"],
        [f"Phone: {customer.phone}"],
    ]
    
    customer_table = Table(customer_info, colWidths=[5*inch])
    customer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Product table
    elements.append(Paragraph("Product Details:", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))
    
    data = [['Product', 'Qty', 'Unit Price', 'Discount', 'Total']]
    
    for item in items:
        data.append([
            item.product.product_name,
            str(item.quantity),
            f"Rs.{item.unit_price:,.2f}",
            f"{item.discount_percentage}%",
            f"Rs.{item.line_total:,.2f}"
        ])
    
    # Totals
    data.append(['', '', 'Subtotal:', '', f"Rs.{quotation.total_list_price:,.2f}"])
    data.append(['', '', 'Discount:', '', f"-Rs.{quotation.discount_amount:,.2f}"])
    data.append(['', '', 'Total:', '', f"Rs.{quotation.final_price:,.2f}"])
    
    product_table = Table(data, colWidths=[2.5*inch, 0.5*inch, 1*inch, 0.75*inch, 1.25*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -3), (-1, -1), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(product_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Terms and conditions
    elements.append(Paragraph("Terms & Conditions:", styles['Heading3']))
    terms = [
        "1. This quotation is valid until the date mentioned above.",
        "2. Prices are exclusive of GST and other applicable taxes.",
        "3. Payment terms: 50% advance, 50% on delivery.",
        "4. Subject to Ampalone Master Agreement and SLA.",
        "5. Delivery timeline: 2-4 weeks from payment confirmation."
    ]
    
    for term in terms:
        elements.append(Paragraph(term, styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Documents reference
    elements.append(Paragraph("Attached Documents:", styles['Heading3']))
    documents = [
        "- Ampalone Non-Disclosure Agreement (NDA)",
        "- Ampalone Master Service Agreement (MSA)",
        "- Service Level Agreement (SLA)"
    ]
    
    for doc in documents:
        elements.append(Paragraph(doc, styles['Normal']))
    
    # Footer
    elements.append(Spacer(1, 1*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        "Ampalone Softwares Private Limited | CIN: U72200KA2020PTC134567 | www.ampalone.com",
        footer_style
    ))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer
