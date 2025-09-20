from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

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
    """Serve frontend index if present; else JSON status."""
    import os
    index_path = os.path.join("automa", "web", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"app": settings.app_name, "status": "ok"}


# Static files and favicon
app.mount("/static", StaticFiles(directory="automa/web/static", check_dir=False), name="static")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Prefer project static dir; fallback to repo root for existing file
    import os

    candidates = [
        os.path.join("automa", "web", "static", "favicon.ico"),
        os.path.join("favicon.ico"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return FileResponse(path)
    # No favicon found
    return FileResponse(os.devnull)


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(agents.router)
app.include_router(scripts.router)
app.include_router(jobs.router)
