"""
Transfer API Endpoints
CRUD operations for managing asset transfers between units
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime

from app.db.session import get_db
from app.models.transfer import Transfer
from app.models.asset import Asset
from app.schemas.transfer import TransferCreate, TransferUpdate, TransferResponse
from app.middleware.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/transfers",
    tags=["Transfers"]
)


@router.get("/", response_model=List[TransferResponse])
def list_transfers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    unit_id: int = Query(None, description="Filter by unit (from or to)"),
    status_filter: str = Query(None, description="Filter by status"),
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all transfers with filters"""
    query = db.query(Transfer)
    
    if unit_id:
        query = query.filter(
            (Transfer.from_unit_id == unit_id) | (Transfer.to_unit_id == unit_id)
        )
    if status_filter:
        query = query.filter(Transfer.status == status_filter)
    if start_date:
        query = query.filter(Transfer.transfer_date >= start_date)
    if end_date:
        query = query.filter(Transfer.transfer_date <= end_date)
    
    transfers = query.order_by(Transfer.transfer_date.desc()).offset(skip).limit(limit).all()
    return transfers


@router.get("/{transfer_id}", response_model=TransferResponse)
def get_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific transfer by ID"""
    transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transfer with id {transfer_id} not found"
        )
    return transfer


@router.post("/", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(
    transfer_data: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new transfer request
    """
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == transfer_data.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with id {transfer_data.asset_id} not found"
        )
    
    # Verify sufficient quantity at source unit
    if asset.unit_id != transfer_data.from_unit_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset not located at source unit"
        )
    
    if asset.quantity < transfer_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient quantity. Available: {asset.quantity}, Requested: {transfer_data.quantity}"
        )
    
    # Create transfer record
    db_transfer = Transfer(
        **transfer_data.model_dump(),
        initiated_by=current_user.id
    )
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    
    return db_transfer


@router.put("/{transfer_id}", response_model=TransferResponse)
def update_transfer_status(
    transfer_id: int,
    update_data: TransferUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update transfer status (approve, complete, cancel)
    """
    transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transfer with id {transfer_id} not found"
        )
    
    # Update status
    transfer.status = update_data.status
    
    if update_data.approved_by:
        transfer.approved_by = update_data.approved_by
    
    # If completed, update asset location
    if update_data.status == "COMPLETED":
        transfer.completed_at = datetime.utcnow()
        
        # Update asset unit_id
        asset = db.query(Asset).filter(Asset.id == transfer.asset_id).first()
        if asset:
            asset.unit_id = transfer.to_unit_id
    
    db.commit()
    db.refresh(transfer)
    
    return transfer


@router.delete("/{transfer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a transfer record"""
    transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transfer with id {transfer_id} not found"
        )
    
    db.delete(transfer)
    db.commit()
    
    return None
