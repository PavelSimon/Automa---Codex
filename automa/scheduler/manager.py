from datetime import datetime
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler


_scheduler: Optional[BackgroundScheduler] = None


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


def _run_job(job_id: int):
    # TODO: integrate with sandbox runner to execute the script
    # placeholder: mark as executed, logging handled elsewhere
    print(f"Executing job {job_id}")


def scheduler_add_once(job_id: int, when: datetime | None):
    sched = get_scheduler()
    run_date = when or datetime.now()
    sched.add_job(_run_job, "date", run_date=run_date, args=[job_id], id=f"job-{job_id}")

