"""
Purchase API Endpoints
CRUD operations for managing asset purchases
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List
from datetime import date, datetime

from app.db.session import get_db
from app.models.purchase import Purchase
from app.models.asset import Asset
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.middleware.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/purchases",
    tags=["Purchases"]
)


@router.get("/", response_model=List[PurchaseResponse])
def list_purchases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    unit_id: int = Query(None, description="Filter by unit"),
    category_id: int = Query(None, description="Filter by category"),
    start_date: date = Query(None, description="Start date filter"),
    end_date: date = Query(None, description="End date filter"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all purchases with filters"""
    query = db.query(Purchase)
    
    if unit_id:
        query = query.filter(Purchase.unit_id == unit_id)
    if category_id:
        query = query.filter(Purchase.category_id == category_id)
    if start_date:
        query = query.filter(Purchase.purchase_date >= start_date)
    if end_date:
        query = query.filter(Purchase.purchase_date <= end_date)
    
    purchases = query.order_by(Purchase.purchase_date.desc()).offset(skip).limit(limit).all()
    return purchases


@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific purchase by ID"""
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with id {purchase_id} not found"
        )
    return purchase


@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(
    purchase_data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new purchase record
    This will also update the asset quantity
    """
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == purchase_data.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with id {purchase_data.asset_id} not found"
        )
    
    # Calculate total amount
    total_amount = purchase_data.quantity * purchase_data.unit_price
    
    # Create purchase record
    db_purchase = Purchase(
        **purchase_data.model_dump(),
        total_amount=total_amount,
        created_by=current_user.id
    )
    db.add(db_purchase)
    
    # Update asset quantity
    asset.quantity += purchase_data.quantity
    
    db.commit()
    db.refresh(db_purchase)
    
    return db_purchase


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a purchase record"""
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with id {purchase_id} not found"
        )
    
    db.delete(purchase)
    db.commit()
    
    return None
