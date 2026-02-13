"""
Unit/Base Model
Represents military bases/units in the system
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Unit(Base):
    """Unit/Base model for military installations"""
    
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    location = Column(String(200), nullable=False)
    commander_id = Column(Integer, nullable=True)  # Reference to user
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Unit(id={self.id}, name='{self.name}', code='{self.code}')>"
