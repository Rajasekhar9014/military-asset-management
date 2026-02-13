"""
Asset Model
Represents military assets (weapons, vehicles, equipment, etc.)
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Asset(Base):
    """Asset model for military equipment and supplies"""
    
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("asset_categories.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True, index=True)
    
    # Asset details
    serial_number = Column(String(100), unique=True, nullable=True, index=True)
    description = Column(Text, nullable=True)
    unit_price = Column(Numeric(15, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    
    # Status
    status = Column(String(50), nullable=False, default="AVAILABLE", index=True)
    # Status options: AVAILABLE, ASSIGNED, IN_TRANSIT, EXPENDED, MAINTENANCE
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Asset(id={self.id}, name='{self.name}', quantity={self.quantity})>"
