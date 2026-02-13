"""
Assignment and Expenditure Models
Represents asset assignments to personnel and expenditures
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.sql import func

from app.db.session import Base


class Assignment(Base):
    """Assignment model for tracking assets assigned to personnel"""
    
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    
    # Assignment details
    assigned_to = Column(String(200), nullable=False)  # Personnel name/ID
    quantity = Column(Integer, nullable=False)
    assignment_date = Column(Date, nullable=False, index=True)
    return_date = Column(Date, nullable=True)
    
    # Status
    status = Column(String(50), nullable=False, default="ACTIVE", index=True)
    # Status options: ACTIVE, RETURNED, LOST, DAMAGED
    
    # Additional info
    purpose = Column(String(500), nullable=True)
    notes = Column(String(500), nullable=True)
    
    # Audit
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Assignment(id={self.id}, asset_id={self.asset_id}, assigned_to='{self.assigned_to}')>"


class Expenditure(Base):
    """Expenditure model for tracking consumed/expended assets"""
    
    __tablename__ = "expenditures"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    
    # Expenditure details
    quantity = Column(Integer, nullable=False)
    expenditure_date = Column(Date, nullable=False, index=True)
    
    # Additional info
    reason = Column(String(500), nullable=False)
    activity = Column(String(200), nullable=True)  # Training, Operation, etc.
    notes = Column(String(500), nullable=True)
    
    # Audit
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Expenditure(id={self.id}, asset_id={self.asset_id}, quantity={self.quantity})>"
