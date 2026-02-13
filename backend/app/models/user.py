from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.db.session import Base


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    
    # Role and unit (simplified for now, can expand later)
    role_id = Column(Integer, nullable=False, default=1)
    unit_id = Column(Integer, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role_id": self.role_id,
            "unit_id": self.unit_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
