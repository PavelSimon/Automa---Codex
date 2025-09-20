from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from ...api.deps import get_db
from ...core.security import authenticate_user, create_access_token
from ...domain.models import Agent, Script, Job, User
from ...scheduler.manager import scheduler_add_once


templates = Jinja2Templates(directory="automa/web/templates")
router = APIRouter(prefix="/ui", tags=["ui"])


def _get_user_from_cookie(request: Request, session: Session) -> Optional[User]:
    token = request.cookies.get("automa_access_token")
    if not token:
        return None
    # Lazy import to reuse logic
    from jose import JWTError, jwt
    from ...core.config import settings
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")
        if not email:
            return None
        return session.exec(select(User).where(User.email == email)).first()
    except JWTError:
        return None


@router.post("/auth/login", response_class=HTMLResponse)
def ui_login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_db),
):
    user = authenticate_user(session, email, password)
    if not user:
        # Return small snippet with error
        return HTMLResponse("<span class='err'>Nesprávne prihlasovacie údaje</span>", status_code=401)
    token = create_access_token({"sub": user.email})
    # Cookie for UI requests
    response.set_cookie("automa_access_token", token, httponly=True, samesite="lax")
    return templates.TemplateResponse("partials/login_status.html", {"request": request, "user": user})


@router.post("/auth/logout", response_class=HTMLResponse)
def ui_logout(request: Request, response: Response):
    response.delete_cookie("automa_access_token")
    return HTMLResponse("<span>Odhlásený</span>")


@router.get("/partials/login_status", response_class=HTMLResponse)
def login_status(request: Request, session: Session = Depends(get_db)):
    user = _get_user_from_cookie(request, session)
    return templates.TemplateResponse("partials/login_status.html", {"request": request, "user": user})


@router.get("/partials/agents", response_class=HTMLResponse)
def partial_agents(request: Request, session: Session = Depends(get_db)):
    agents = session.exec(select(Agent)).all()
    return templates.TemplateResponse("partials/agents_list.html", {"request": request, "agents": agents})


@router.post("/agents", response_class=HTMLResponse)
def create_agent_ui(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    session: Session = Depends(get_db),
):
    user = _get_user_from_cookie(request, session)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    agent = Agent(name=name, description=description)
    session.add(agent)
    session.commit()
    agents = session.exec(select(Agent)).all()
    return templates.TemplateResponse("partials/agents_list.html", {"request": request, "agents": agents})


@router.get("/partials/scripts", response_class=HTMLResponse)
def partial_scripts(request: Request, session: Session = Depends(get_db)):
    scripts = session.exec(select(Script)).all()
    return templates.TemplateResponse("partials/scripts_list.html", {"request": request, "scripts": scripts})


@router.post("/scripts", response_class=HTMLResponse)
def create_script_ui(
    request: Request,
    name: str = Form(...),
    path: str = Form(...),
    description: Optional[str] = Form(None),
    session: Session = Depends(get_db),
):
    user = _get_user_from_cookie(request, session)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    script = Script(name=name, path=path, description=description)
    session.add(script)
    session.commit()
    scripts = session.exec(select(Script)).all()
    return templates.TemplateResponse("partials/scripts_list.html", {"request": request, "scripts": scripts})


@router.get("/partials/jobs", response_class=HTMLResponse)
def partial_jobs(request: Request, session: Session = Depends(get_db)):
    jobs = session.exec(select(Job)).all()
    return templates.TemplateResponse("partials/jobs_list.html", {"request": request, "jobs": jobs})


@router.post("/jobs", response_class=HTMLResponse)
def create_job_ui(
    request: Request,
    script_id: Optional[int] = Form(None),
    when: Optional[str] = Form(None),
    session: Session = Depends(get_db),
):
    user = _get_user_from_cookie(request, session)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    job = Job(script_id=script_id, status="scheduled")
    session.add(job)
    session.commit()
    # schedule
    dt = None
    if when:
        try:
            dt = datetime.fromisoformat(when)
        except ValueError:
            dt = None
    scheduler_add_once(job_id=job.id, when=dt)

    jobs = session.exec(select(Job)).all()
    return templates.TemplateResponse("partials/jobs_list.html", {"request": request, "jobs": jobs})

