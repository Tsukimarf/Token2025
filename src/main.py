"""
src/main.py

FastAPI application entrypoint. Run with:
    uvicorn main:app --reload

Install dependencies:
    pip install fastapi uvicorn sqlalchemy pydantic[email] python-jose passlib[bcrypt] python-dotenv
"""

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import settings
from database import engine, get_db, Base
import models
import schemas
from security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_username,
)

# Create tables (for simple projects; use Alembic migrations for production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "env": settings.ENV, "status": "ok"}


# --- Auth routes ------------------------------------------------------------

@app.post("/auth/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.username == user_in.username) | (models.User.email == user_in.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=schemas.Token)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=token)


# --- Protected example route ------------------------------------------------

@app.get("/users/me", response_model=schemas.UserOut)
def read_current_user(
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
