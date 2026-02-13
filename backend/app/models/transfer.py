"""
Transfer Model
Represents asset transfers between bases
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.sql import func

from app.db.session import Base


class Transfer(Base):
    """Transfer model for asset movements between units"""
    
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    
    # Transfer details
    from_unit_id = Column(Integer, ForeignKey("units.id"), nullable=True, index=True)
    to_unit_id = Column(Integer, ForeignKey("units.id"), nullable=True, index=True)
    quantity = Column(Integer, nullable=False)
    transfer_date = Column(Date, nullable=False, index=True)
    
    # Status
    status = Column(String(50), nullable=False, default="PENDING", index=True)
    # Status options: PENDING, IN_TRANSIT, COMPLETED, CANCELLED
    
    # Additional info
    reason = Column(String(500), nullable=True)
    notes = Column(String(500), nullable=True)
    
    # Audit
    initiated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Transfer(id={self.id}, from_unit={self.from_unit_id}, to_unit={self.to_unit_id})>"
