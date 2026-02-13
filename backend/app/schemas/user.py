"""User management schemas"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=100)
    role_id: int = Field(default=1, ge=1)
    unit_id: Optional[int] = Field(None, ge=1)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Username must be alphanumeric with underscores"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "username": "john_doe",
            "email": "john.doe@military.mil",
            "password": "SecurePass123",
            "full_name": "John Doe",
            "role_id": 2,
            "unit_id": 5
        }
    }}


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role_id: Optional[int] = Field(None, ge=1)
    unit_id: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    full_name: str
    role_id: int
    unit_id: Optional[int]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    model_config = {"from_attributes": True}


class ChangePasswordRequest(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v
