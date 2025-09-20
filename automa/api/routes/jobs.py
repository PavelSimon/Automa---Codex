from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ...api.deps import get_db
from ...core.security import get_current_user
from ...domain.models import Job, User, Script
from ...scheduler.manager import scheduler_add_once


class JobCreate(BaseModel):
    script_id: int | None = None
    when: datetime | None = None  # if None, run asap


router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


@router.get("")
def list_jobs(session: Session = Depends(get_db)):
    return session.exec(select(Job)).all()


@router.post("")
def create_job(payload: JobCreate, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = Job(script_id=payload.script_id, status="scheduled")
    session.add(job)
    session.commit()
    session.refresh(job)

    # schedule a one-off execution (stub)
    try:
        scheduler_add_once(job_id=job.id, when=payload.when)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scheduler error: {e}")
    return job

