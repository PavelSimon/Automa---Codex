from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine
from .config import settings


engine = create_engine(settings.sqlite_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session

