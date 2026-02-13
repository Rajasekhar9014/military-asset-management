"""
Purchase Pydantic Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class PurchaseBase(BaseModel):
    """Base schema for purchase"""
    asset_id: int = Field(..., description="Asset ID")
    unit_id: int = Field(..., description="Unit/Base ID")
    category_id: int = Field(..., description="Category ID")
    quantity: int = Field(..., gt=0, description="Quantity purchased")
    unit_price: Decimal = Field(..., gt=0, description="Price per unit")
    purchase_date: date = Field(..., description="Purchase date")
    vendor: Optional[str] = Field(None, max_length=200)
    invoice_number: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)


class PurchaseCreate(PurchaseBase):
    """Schema for creating a purchase"""
    pass


class PurchaseResponse(PurchaseBase):
    """Schema for purchase response"""
    id: int
    total_amount: Decimal
    created_by: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
