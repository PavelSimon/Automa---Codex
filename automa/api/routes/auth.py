from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ...core.security import create_access_token, authenticate_user, get_password_hash
from ...core.config import settings
from ..deps import get_db
from ...domain.models import User
from pydantic import BaseModel, EmailStr


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": token, "token_type": "bearer"}


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


@router.post("/register")
def register(payload: RegisterRequest, session: Session = Depends(get_db)):
    from sqlmodel import select

    if session.exec(select(User).where(User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=get_password_hash(payload.password), full_name=payload.full_name, is_active=True)
    session.add(user)
    session.commit()
    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": token, "token_type": "bearer"}
