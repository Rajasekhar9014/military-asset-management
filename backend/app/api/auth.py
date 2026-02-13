"""Authentication API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    - **username**: User's username
    - **password**: User's password
    
    Returns access token and user information.
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "role_id": user.role_id
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }
