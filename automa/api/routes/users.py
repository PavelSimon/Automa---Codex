from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..deps import get_db
from ...core.security import (
    get_current_user,
    verify_password,
    get_password_hash,
)
from ...domain.models import User


router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=None)
def read_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin}


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None


@router.patch("/me")
def update_me(
    payload: UserUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.email and payload.email != current_user.email:
        if session.exec(select(User).where(User.email == payload.email)).first():
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = payload.email
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return {"email": current_user.email, "full_name": current_user.full_name}


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


@router.post("/me/change_password")
def change_password(
    payload: PasswordChange,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid current password")
    current_user.hashed_password = get_password_hash(payload.new_password)
    session.add(current_user)
    session.commit()
    return {"status": "ok"}
