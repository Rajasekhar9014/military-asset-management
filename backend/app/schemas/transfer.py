"""
Transfer Pydantic Schemas
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime, date
from typing import Optional


class TransferBase(BaseModel):
    """Base schema for transfer"""
    asset_id: int = Field(..., description="Asset ID")
    from_unit_id: int = Field(..., description="Source unit ID")
    to_unit_id: int = Field(..., description="Destination unit ID")
    quantity: int = Field(..., gt=0, description="Quantity to transfer")
    transfer_date: date = Field(..., description="Transfer date")
    reason: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=500)
    
    @field_validator('to_unit_id')
    @classmethod
    def validate_different_units(cls, v, info):
        if 'from_unit_id' in info.data and v == info.data['from_unit_id']:
            raise ValueError('Cannot transfer to the same unit')
        return v


class TransferCreate(TransferBase):
    """Schema for creating a transfer"""
    pass


class TransferUpdate(BaseModel):
    """Schema for updating transfer status"""
    status: str = Field(..., pattern="^(PENDING|IN_TRANSIT|COMPLETED|CANCELLED)$")
    approved_by: Optional[int] = None


class TransferResponse(TransferBase):
    """Schema for transfer response"""
    id: int
    status: str
    initiated_by: int
    approved_by: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)
