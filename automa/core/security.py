from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from .config import settings
from ..domain.models import User
from ..api.deps import get_db


_pwd_context: CryptContext | None = None


def _build_pwd_context() -> CryptContext:
    # Try bcrypt first; fall back to pbkdf2_sha256 if unavailable
    try:
        import bcrypt  # noqa: F401
        return CryptContext(schemes=["bcrypt"], deprecated="auto")
    except Exception:
        return CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_pwd_context() -> CryptContext:
    global _pwd_context
    if _pwd_context is None:
        _pwd_context = _build_pwd_context()
    return _pwd_context
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_pwd_context().verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return get_pwd_context().hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        sub: str | None = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.email == sub)).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user
