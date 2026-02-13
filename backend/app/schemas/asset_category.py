"""
Asset Category Pydantic Schemas
Validation and serialization schemas for asset categories
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AssetCategoryBase(BaseModel):
    """Base schema for asset category"""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    code: str = Field(..., min_length=2, max_length=20, description="Category code (e.g., WPN, VEH)")


class AssetCategoryCreate(AssetCategoryBase):
    """Schema for creating a new asset category"""
    pass


class AssetCategoryUpdate(BaseModel):
    """Schema for updating an asset category"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    code: Optional[str] = Field(None, min_length=2, max_length=20)


class AssetCategoryResponse(AssetCategoryBase):
    """Schema for asset category response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AssetCategoryList(BaseModel):
    """Schema for paginated list of asset categories"""
    total: int
    categories: list[AssetCategoryResponse]
