"""
Asset Category Model
Represents categories for military assets (e.g., Weapons, Vehicles, Equipment)
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class AssetCategory(Base):
    """Asset Category model for categorizing military assets"""
    
    __tablename__ = "asset_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "WPN", "VEH", "EQP"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships (will be added when Asset model is created)
    # assets = relationship("Asset", back_populates="category")
    
    def __repr__(self):
        return f"<AssetCategory(id={self.id}, name='{self.name}', code='{self.code}')>"
