"""
src/schemas.py

Pydantic schemas used for request validation and response shaping.
These are separate from the SQLAlchemy models in models.py so the
API contract can evolve independently of the database structure.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# --- User ---------------------------------------------------------------

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows creation from SQLAlchemy objects


# --- Auth -----------------------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
