"""
Purchase Model
Represents asset purchases for a base
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Date
from sqlalchemy.sql import func

from app.db.session import Base


class Purchase(Base):
    """Purchase model for recording asset acquisitions"""
    
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    unit_id = Column(Integer, nullable=True, index=True)  # Foreign key to units table (not yet implemented)
    category_id = Column(Integer, ForeignKey("asset_categories.id"), nullable=False, index=True)
    
    # Purchase details
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    total_amount = Column(Numeric(15, 2), nullable=False)
    purchase_date = Column(Date, nullable=False, index=True)
    
    # Additional info
    vendor = Column(String(200), nullable=True)
    invoice_number = Column(String(100), nullable=True)
    notes = Column(String(500), nullable=True)
    
    # Audit
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Purchase(id={self.id}, asset_id={self.asset_id}, quantity={self.quantity})>"
