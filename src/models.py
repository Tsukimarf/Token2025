"""
src/models.py

SQLAlchemy ORM models. Import this module (so Base.metadata knows
about these tables) before calling init_db() in database.py.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
