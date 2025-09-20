from datetime import datetime, timezone
from typing import Optional
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from ..core.db import get_session
from ..domain.models import Job, Script
from ..sandbox.docker_runner import run_script


_scheduler: Optional[BackgroundScheduler] = None
_logger = logging.getLogger(__name__)


def get_scheduler() -> BackgroundScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
    return _scheduler


def scheduler_start():
    sched = get_scheduler()
    if not sched.running:
        sched.start()


def scheduler_shutdown():
    sched = get_scheduler()
    if sched.running:
        sched.shutdown(wait=False)


def execute_job(job_id: int) -> None:
    """Run the job inside the sandbox and persist execution metadata."""
    now = datetime.now(timezone.utc)

    script_path: str | None = None
    with get_session() as session:
        job = session.get(Job, job_id)
        if job is None:
            _logger.warning("Attempted to execute missing job %s", job_id)
            return

        job.status = "running"
        job.last_error = None
        session.add(job)
        session.commit()

        if job.script_id is None:
            job.status = "failed"
            job.last_run_at = now
            job.last_exit_code = None
            job.last_error = "No script linked to job"
            session.add(job)
            session.commit()
            return

        script = session.get(Script, job.script_id)
        if script is None:
            job.status = "failed"
            job.last_run_at = now
            job.last_exit_code = None
            job.last_error = "Script not found"
            session.add(job)
            session.commit()
            return

        script_path = script.path

    exit_code = 1
    error_message: str | None = None
    try:
        assert script_path is not None  # for type checkers; guarded above
        exit_code = run_script(script_path, args=None)
    except Exception as exc:  # pragma: no cover - just in case sandbox explodes
        error_message = str(exc)
        _logger.exception("Job %s failed during sandbox execution", job_id)

    with get_session() as session:
        job = session.get(Job, job_id)
        if job is None:
            _logger.warning("Job %s disappeared before completion update", job_id)
            return

        job.last_run_at = now
        job.last_exit_code = exit_code
        if exit_code == 0 and error_message is None:
            job.status = "succeeded"
            job.last_error = None
        else:
            job.status = "failed"
            job.last_error = error_message or f"Exit code {exit_code}"

        session.add(job)
        session.commit()


def scheduler_add_once(job_id: int, when: datetime | None):
    sched = get_scheduler()
    run_date = when or datetime.now(timezone.utc)
    if run_date.tzinfo is None:
        run_date = run_date.replace(tzinfo=timezone.utc)
    sched.add_job(
        execute_job,
        "date",
        run_date=run_date,
        args=[job_id],
        id=f"job-{job_id}",
        replace_existing=True,
    )
