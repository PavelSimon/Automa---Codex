from sqlmodel import Session, select
from .models import User
from ..core.security import get_password_hash
from ..core.config import settings


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def ensure_bootstrap_admin(session: Session) -> None:
    """Create default admin if missing (MVP bootstrap)."""
    existing = get_user_by_email(session, settings.admin_email)
    if existing:
        return
    user = User(
        email=settings.admin_email,
        hashed_password=get_password_hash(settings.admin_password),
        is_active=True,
        is_admin=True,
    )
    session.add(user)
    session.commit()

