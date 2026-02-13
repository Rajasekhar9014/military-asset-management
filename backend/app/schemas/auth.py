"""Authentication schemas for request/response validation"""
from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Schema for login request"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=1, description="Password")
    
    model_config = {"json_schema_extra": {
        "example": {
            "username": "admin",
            "password": "Admin123!"
        }
    }}


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    user: dict
    
    model_config = {"json_schema_extra": {
        "example": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "username": "admin",
                "email": "admin@military.mil",
                "full_name": "System Administrator"
            }
        }
    }}


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    full_name: str
    role_id: int
    is_active: bool
    
    model_config = {"from_attributes": True}
