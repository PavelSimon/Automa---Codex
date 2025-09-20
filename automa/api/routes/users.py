from fastapi import APIRouter, Depends
from sqlmodel import Session

from ...core.security import get_current_user
from ...domain.models import User


router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=None)
def read_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin}

