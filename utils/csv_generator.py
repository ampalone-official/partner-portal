# app/utils/csv_generator.py
"""
Ampalone Partner Portal - CSV Generation Utilities
Version: 1.0.0
"""

import csv
from io import StringIO, BytesIO
from typing import List


def generate_quotation_csv(quotation, items: list) -> BytesIO:
    """
    Generate quotation CSV export
    """
    buffer = BytesIO()
    wrapper = StringIO()
    
    # Define CSV columns
    fieldnames = [
        'Quotation Number',
        'Product Code',
        'Product Name',
        'Quantity',
        'Unit Price',
        'Discount %',
        'Line Total',
        'Pricing Model',
        'Term (Months)'
    ]
    
    writer = csv.DictWriter(wrapper, fieldnames=fieldnames)
    writer.writeheader()
    
    # Add line items
    for item in items:
        writer.writerow({
            'Quotation Number': quotation.quotation_number,
            'Product Code': item.product.product_code,
            'Product Name': item.product.product_name,
            'Quantity': item.quantity,
            'Unit Price': item.unit_price,
            'Discount %': item.discount_percentage,
            'Line Total': item.line_total,
            'Pricing Model': item.pricing_model or 'N/A',
            'Term (Months)': item.term_months
        })
    
    # Add totals row
    writer.writerow({
        'Quotation Number': quotation.quotation_number,
        'Product Code': '',
        'Product Name': 'TOTAL',
        'Quantity': '',
        'Unit Price': '',
        'Discount %': quotation.discount_percentage,
        'Line Total': quotation.final_price,
        'Pricing Model': '',
        'Term (Months)': ''
    })
    
    # Convert to bytes
    buffer.write(wrapper.getvalue().encode('utf-8'))
    buffer.seek(0)
    
    return buffer


def generate_partner_report_csv(partners: list) -> BytesIO:
    """
    Generate partner performance report CSV
    """
    buffer = BytesIO()
    wrapper = StringIO()
    
    fieldnames = [
        'Partner ID',
        'Company Name',
        'Partner Tier',
        'Email',
        'Phone',
        'Status',
        'Customers Tagged',
        'Quotations Generated',
        'Total Pipeline Value',
        'Deals Closed',
        'Created Date'
    ]
    
    writer = csv.DictWriter(wrapper, fieldnames=fieldnames)
    writer.writeheader()
    
    for partner in partners:
        writer.writerow({
            'Partner ID': partner.partner_id,
            'Company Name': partner.company_name,
            'Partner Tier': partner.partner_tier,
            'Email': partner.email,
            'Phone': partner.phone,
            'Status': partner.status,
            'Customers Tagged': partner.customers_tagged or 0,
            'Quotations Generated': partner.quotations_generated or 0,
            'Total Pipeline Value': partner.total_pipeline_value or 0,
            'Deals Closed': partner.deals_closed or 0,
            'Created Date': partner.created_at.strftime('%Y-%m-%d') if partner.created_at else ''
        })
    
    buffer.write(wrapper.getvalue().encode('utf-8'))
    buffer.seek(0)
    
    return buffer
