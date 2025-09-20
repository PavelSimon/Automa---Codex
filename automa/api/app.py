from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import settings
from ..core.db import init_db, get_session
from ..domain.repo import ensure_bootstrap_admin
from ..scheduler.manager import scheduler_start, scheduler_shutdown

from .routes import health, auth, users, agents, scripts, jobs


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with get_session() as s:
        ensure_bootstrap_admin(s)
    scheduler_start()


@app.on_event("shutdown")
def on_shutdown() -> None:
    scheduler_shutdown()


@app.get("/")
def root():
    return {"app": settings.app_name, "status": "ok"}


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(agents.router)
app.include_router(scripts.router)
app.include_router(jobs.router)

