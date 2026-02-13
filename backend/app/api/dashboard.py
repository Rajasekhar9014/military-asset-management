"""
Dashboard API Endpoints
Provides metrics and analytics for the dashboard
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date, datetime, timedelta
from decimal import Decimal

from app.db.session import get_db
from app.models.asset import Asset
from app.models.purchase import Purchase
from app.models.transfer import Transfer
from app.models.assignment import Assignment, Expenditure
from app.schemas.dashboard import DashboardMetrics, MovementDetail
from app.middleware.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/metrics", response_model=DashboardMetrics)
def get_dashboard_metrics(
    unit_id: int = Query(None, description="Filter by unit"),
    category_id: int = Query(None, description="Filter by category"),
    start_date: date = Query(None, description="Start date"),
    end_date: date = Query(None, description="End date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard metrics including:
    - Opening Balance
    - Closing Balance
    - Net Movement (Purchases + Transfer In - Transfer Out)
    - Assigned assets
    - Expended assets
    """
    
    # Build base query for assets
    asset_query = db.query(Asset)
    if unit_id:
        asset_query = asset_query.filter(Asset.unit_id == unit_id)
    if category_id:
        asset_query = asset_query.filter(Asset.category_id == category_id)
    
    # Closing balance (current quantity)
    closing_balance = db.query(func.sum(Asset.quantity)).filter(
        and_(
            Asset.unit_id == unit_id if unit_id else True,
            Asset.category_id == category_id if category_id else True
        )
    ).scalar() or 0
    
    # Purchases in date range
    purchase_query = db.query(func.sum(Purchase.quantity))
    if unit_id:
        purchase_query = purchase_query.filter(Purchase.unit_id == unit_id)
    if category_id:
        purchase_query = purchase_query.filter(Purchase.category_id == category_id)
    if start_date:
        purchase_query = purchase_query.filter(Purchase.purchase_date >= start_date)
    if end_date:
        purchase_query = purchase_query.filter(Purchase.purchase_date <= end_date)
    
    purchases = purchase_query.scalar() or 0
    
    # Transfers IN (to this unit)
    transfer_in_query = db.query(func.sum(Transfer.quantity)).filter(
        Transfer.status == "COMPLETED"
    )
    if unit_id:
        transfer_in_query = transfer_in_query.filter(Transfer.to_unit_id == unit_id)
    if start_date:
        transfer_in_query = transfer_in_query.filter(Transfer.transfer_date >= start_date)
    if end_date:
        transfer_in_query = transfer_in_query.filter(Transfer.transfer_date <= end_date)
    
    transfer_in = transfer_in_query.scalar() or 0
    
    # Transfers OUT (from this unit)
    transfer_out_query = db.query(func.sum(Transfer.quantity)).filter(
        Transfer.status == "COMPLETED"
    )
    if unit_id:
        transfer_out_query = transfer_out_query.filter(Transfer.from_unit_id == unit_id)
    if start_date:
        transfer_out_query = transfer_out_query.filter(Transfer.transfer_date >= start_date)
    if end_date:
        transfer_out_query = transfer_out_query.filter(Transfer.transfer_date <= end_date)
    
    transfer_out = transfer_out_query.scalar() or 0
    
    # Assigned assets
    assigned_query = db.query(func.sum(Assignment.quantity)).filter(
        Assignment.status == "ACTIVE"
    )
    if unit_id:
        assigned_query = assigned_query.filter(Assignment.unit_id == unit_id)
    if start_date:
        assigned_query = assigned_query.filter(Assignment.assignment_date >= start_date)
    if end_date:
        assigned_query = assigned_query.filter(Assignment.assignment_date <= end_date)
    
    assigned = assigned_query.scalar() or 0
    
    # Expended assets
    expended_query = db.query(func.sum(Expenditure.quantity))
    if unit_id:
        expended_query = expended_query.filter(Expenditure.unit_id == unit_id)
    if start_date:
        expended_query = expended_query.filter(Expenditure.expenditure_date >= start_date)
    if end_date:
        expended_query = expended_query.filter(Expenditure.expenditure_date <= end_date)
    
    expended = expended_query.scalar() or 0
    
    # Calculate net movement and opening balance
    net_movement = purchases + transfer_in - transfer_out
    opening_balance = closing_balance - net_movement
    
    # Calculate total value
    total_value_query = db.query(func.sum(Asset.quantity * Asset.unit_price))
    if unit_id:
        total_value_query = total_value_query.filter(Asset.unit_id == unit_id)
    if category_id:
        total_value_query = total_value_query.filter(Asset.category_id == category_id)
    
    total_value = total_value_query.scalar() or Decimal('0.00')
    
    return DashboardMetrics(
        opening_balance=opening_balance,
        closing_balance=closing_balance,
        net_movement=net_movement,
        purchases=purchases,
        transfer_in=transfer_in,
        transfer_out=transfer_out,
        assigned=assigned,
        expended=expended,
        total_value=total_value
    )


@router.get("/movement-details", response_model=MovementDetail)
def get_movement_details(
    unit_id: int = Query(None),
    category_id: int = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed breakdown of net movement
    (For pop-up display when clicking Net Movement)
    """
    # Same logic as above but return detailed breakdown
    purchase_query = db.query(func.sum(Purchase.quantity))
    if unit_id:
        purchase_query = purchase_query.filter(Purchase.unit_id == unit_id)
    if category_id:
        purchase_query = purchase_query.filter(Purchase.category_id == category_id)
    if start_date:
        purchase_query = purchase_query.filter(Purchase.purchase_date >= start_date)
    if end_date:
        purchase_query = purchase_query.filter(Purchase.purchase_date <= end_date)
    
    purchases = purchase_query.scalar() or 0
    
    transfer_in_query = db.query(func.sum(Transfer.quantity)).filter(Transfer.status == "COMPLETED")
    if unit_id:
        transfer_in_query = transfer_in_query.filter(Transfer.to_unit_id == unit_id)
    if start_date:
        transfer_in_query = transfer_in_query.filter(Transfer.transfer_date >= start_date)
    if end_date:
        transfer_in_query = transfer_in_query.filter(Transfer.transfer_date <= end_date)
    
    transfer_in = transfer_in_query.scalar() or 0
    
    transfer_out_query = db.query(func.sum(Transfer.quantity)).filter(Transfer.status == "COMPLETED")
    if unit_id:
        transfer_out_query = transfer_out_query.filter(Transfer.from_unit_id == unit_id)
    if start_date:
        transfer_out_query = transfer_out_query.filter(Transfer.transfer_date >= start_date)
    if end_date:
        transfer_out_query = transfer_out_query.filter(Transfer.transfer_date <= end_date)
    
    transfer_out = transfer_out_query.scalar() or 0
    
    net = purchases + transfer_in - transfer_out
    
    return MovementDetail(
        purchases=purchases,
        transfer_in=transfer_in,
        transfer_out=transfer_out,
        net=net
    )
