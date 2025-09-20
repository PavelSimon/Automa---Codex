import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from ..core.config import settings
from ..core.db import init_db, get_session
from ..domain.repo import ensure_bootstrap_admin
from ..scheduler.manager import scheduler_start, scheduler_shutdown

from .routes import health, auth, users, agents, scripts, jobs, ui
from .routes.ui import _get_user_from_cookie


app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory="automa/web/templates")

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
    # Optional bootstrap and scheduler can be disabled via env for debugging on Windows
    try:
        if os.getenv("AUTOMA_DISABLE_BOOTSTRAP", "0") != "1":
            with get_session() as s:
                ensure_bootstrap_admin(s)
    except Exception as e:
        # Surface startup errors early
        import traceback
        traceback.print_exc()
        raise
    if os.getenv("AUTOMA_DISABLE_SCHED", "0") != "1":
        scheduler_start()


@app.on_event("shutdown")
def on_shutdown() -> None:
    scheduler_shutdown()


@app.get("/")
def root(request: Request):
    with get_session() as s:
        user = _get_user_from_cookie(request, s)
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name, "user": user})


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
app.include_router(ui.router)
