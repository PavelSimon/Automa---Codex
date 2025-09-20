from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...api.deps import get_db
from ...core.security import get_current_user
from ...domain.models import Script, User


router = APIRouter(prefix="/api/v1/scripts", tags=["scripts"])


@router.get("")
def list_scripts(session: Session = Depends(get_db)):
    return session.exec(select(Script)).all()


@router.post("")
def create_script(script: Script, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    script.id = None
    session.add(script)
    session.commit()
    session.refresh(script)
    return script

