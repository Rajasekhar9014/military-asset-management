"""
Asset Category API Endpoints
CRUD operations for managing asset categories
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.asset_category import AssetCategory
from app.schemas.asset_category import (
    AssetCategoryCreate,
    AssetCategoryUpdate,
    AssetCategoryResponse,
    AssetCategoryList
)
from app.middleware.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Asset Categories"]
)


@router.get("/", response_model=List[AssetCategoryResponse])
def list_categories(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all asset categories with pagination
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    categories = db.query(AssetCategory).offset(skip).limit(limit).all()
    return categories


@router.get("/{category_id}", response_model=AssetCategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific asset category by ID
    
    - **category_id**: The ID of the category to retrieve
    """
    category = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with id {category_id} not found"
        )
    return category


@router.post("/", response_model=AssetCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: AssetCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new asset category
    
    - **name**: Category name (unique)
    - **description**: Optional description
    - **code**: Category code (unique, e.g., WPN, VEH)
    """
    # Check if category with same name or code already exists
    existing_name = db.query(AssetCategory).filter(AssetCategory.name == category_data.name).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category_data.name}' already exists"
        )
    
    existing_code = db.query(AssetCategory).filter(AssetCategory.code == category_data.code).first()
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with code '{category_data.code}' already exists"
        )
    
    # Create new category
    db_category = AssetCategory(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.put("/{category_id}", response_model=AssetCategoryResponse)
def update_category(
    category_id: int,
    category_data: AssetCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing asset category
    
    - **category_id**: The ID of the category to update
    - **name**: New category name (optional)
    - **description**: New description (optional)
    - **code**: New category code (optional)
    """
    # Get existing category
    category = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with id {category_id} not found"
        )
    
    # Update fields
    update_data = category_data.model_dump(exclude_unset=True)
    
    # Check for unique constraints if name or code is being updated
    if "name" in update_data:
        existing = db.query(AssetCategory).filter(
            AssetCategory.name == update_data["name"],
            AssetCategory.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{update_data['name']}' already exists"
            )
    
    if "code" in update_data:
        existing = db.query(AssetCategory).filter(
            AssetCategory.code == update_data["code"],
            AssetCategory.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with code '{update_data['code']}' already exists"
            )
    
    # Apply updates
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an asset category
    
    - **category_id**: The ID of the category to delete
    """
    category = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with id {category_id} not found"
        )
    
    # TODO: Check if category has associated assets before deleting
    # For now, we'll allow deletion
    
    db.delete(category)
    db.commit()
    
    return None
