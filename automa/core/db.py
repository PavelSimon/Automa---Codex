from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine
from .config import settings


engine = create_engine(settings.sqlite_url, echo=False)


def _ensure_sqlite_schema() -> None:
    """
    Minimal, idempotent SQLite migrations for existing databases created
    before new columns were added to models. This avoids crashes like
    "no such column: user.full_name" on startup.

    Only runs for SQLite URLs and only performs additive ALTER TABLE
    operations that are safe and idempotent.
    """
    url = str(settings.sqlite_url)
    if not url.startswith("sqlite"):
        return
    with engine.begin() as conn:
        def ensure_columns(table: str, column_defs: dict[str, str]) -> None:
            try:
                existing = {
                    row[1]
                    for row in conn.exec_driver_sql(
                        f"PRAGMA table_info('{table}')"
                    ).fetchall()
                }
            except Exception:
                # Table might not exist yet; create_all will handle it later.
                return

            for column, ddl in column_defs.items():
                if column not in existing:
                    conn.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {ddl}")

        ensure_columns(
            "user",
            {
                "full_name": "full_name TEXT",
                "created_at": "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "is_active": "is_active INTEGER DEFAULT 1",
                "is_admin": "is_admin INTEGER DEFAULT 0",
            },
        )

        ensure_columns(
            "job",
            {
                "last_run_at": "last_run_at TIMESTAMP",
                "last_exit_code": "last_exit_code INTEGER",
                "last_error": "last_error TEXT",
            },
        )


def init_db() -> None:
    # Create tables that don't exist yet
    SQLModel.metadata.create_all(engine)
    # Perform minimal additive migrations for existing SQLite DBs
    _ensure_sqlite_schema()


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
