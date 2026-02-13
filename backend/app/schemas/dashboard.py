"""
Dashboard Pydantic Schemas
"""
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class DashboardMetrics(BaseModel):
    """Dashboard metrics response"""
    opening_balance: int
    closing_balance: int
    net_movement: int
    purchases: int
    transfer_in: int
    transfer_out: int
    assigned: int
    expended: int
    total_value: Decimal


class DashboardFilters(BaseModel):
    """Dashboard filter parameters"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    unit_id: Optional[int] = None
    category_id: Optional[int] = None


class MovementDetail(BaseModel):
    """Detailed movement breakdown"""
    purchases: int
    transfer_in: int
    transfer_out: int
    net: int
