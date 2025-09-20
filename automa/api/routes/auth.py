from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ...core.security import create_access_token, authenticate_user, get_password_hash
from ...core.config import settings
from ..deps import get_db
from ...domain.models import User
from pydantic import BaseModel
from fastapi import Body


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(
    email: str = Body(...),
    password: str = Body(...),
    full_name: str | None = Body(None),
    session: Session = Depends(get_db),
):
    from sqlmodel import select

    if session.exec(select(User).where(User.email == email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, hashed_password=get_password_hash(password), full_name=full_name, is_active=True)
    session.add(user)
    session.commit()
    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": token, "token_type": "bearer"}
