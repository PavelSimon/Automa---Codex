from datetime import datetime, timezone
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
    if payload.script_id is not None:
        if session.get(Script, payload.script_id) is None:
            raise HTTPException(status_code=404, detail="Script not found")

    run_at = payload.when
    if run_at is not None and run_at.tzinfo is None:
        run_at = run_at.replace(tzinfo=timezone.utc)

    job = Job(script_id=payload.script_id, status="scheduled")
    if run_at is not None:
        job.schedule = run_at.isoformat()
    session.add(job)
    session.commit()
    session.refresh(job)

    # schedule a one-off execution (stub)
    try:
        scheduler_add_once(job_id=job.id, when=run_at)
    except Exception as e:
        job.status = "failed"
        job.last_error = f"Scheduler error: {e}"
        session.add(job)
        session.commit()
        raise HTTPException(status_code=500, detail=f"Scheduler error: {e}")
    return job
