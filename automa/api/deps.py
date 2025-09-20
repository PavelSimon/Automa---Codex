from typing import Generator
from ..core.db import get_session


def get_db() -> Generator:
    with get_session() as session:
        yield session

