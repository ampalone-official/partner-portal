# app/models/product.py
"""
Ampalone Partner Portal - Product Model
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    """Product model for Ampalone products"""
    
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(20), unique=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    category = Column(String(50))
    description = Column(Text)
    list_price = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    pricing_model = Column(String(50))
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    pricing_configs = relationship("PricingConfig", back_populates="product")
    quotation_items = relationship("QuotationItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product {self.product_name}>"


class PricingConfig(Base):
    """Pricing configuration for products"""
    
    __tablename__ = "pricing_config"
    
    pricing_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    list_price = Column(Float, nullable=False)
    partner_price = Column(Float, nullable=False)
    min_discount = Column(Float, default=0)
    max_discount_without_approval = Column(Float, default=60)
    currency = Column(String(3), default="INR")
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("Product", back_populates="pricing_configs")
