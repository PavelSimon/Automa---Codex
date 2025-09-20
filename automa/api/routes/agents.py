from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...api.deps import get_db
from ...core.security import get_current_user
from ...domain.models import Agent, User


router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


@router.get("")
def list_agents(session: Session = Depends(get_db)):
    agents = session.exec(select(Agent)).all()
    return agents


@router.post("")
def create_agent(agent: Agent, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    agent.id = None
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent

