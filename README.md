# Automa — Správa Python agentov a úloh

Automa je FastAPI backend pre riadenie, plánovanie, monitoring a audit Python skriptov/agentov. Dôraz je na bezpečnosť (JWT, sandbox stub), rozšíriteľnosť (pluginy) a jednoduché lokálne nasadenie.

## Štruktúra
- `automa/api/`: FastAPI aplikácia a routery (`auth`, `users`, `agents`, `scripts`, `jobs`, `health`).
- `automa/core/`: konfigurácia, DB (SQLModel + SQLite), bezpečnosť (JWT, heslá).
- `automa/domain/`: modely a repo helpery (bootstrap admin).
- `automa/scheduler/`: APScheduler (spúšťanie jednorazových jobov – stub).
- `automa/sandbox/`: adaptér pre bezpečné spúšťanie (Docker/Podman – stub).
- `automa/web/static/`: statické súbory pre jednoduchý frontend (`/static`, `/favicon.ico`).
- `tests/`: pytest testy; `scripts/smoke_test.py`: rýchly smoke.

## Spustenie backendu (uv)
- Pin Python: `uv python pin 3.13`
- Inštalácia: `uv sync`
- Štart API: `uv run uvicorn automa.api.app:app --reload --port 7999`
- Health: `http://localhost:7999/api/v1/health` → `{ "status": "ok" }`

## Frontend
- Statika je servovaná z `automa/web/static` na ceste `/static` a favicon cez `/favicon.ico`.
- Jednoduchý dashboard je voliteľný; pridajte HTML/JS/CSS do `automa/web/static/`.

## Testy
- Spustenie: `uv run pytest -q`
- Zahrnuté: `tests/test_health.py`, `tests/test_auth_and_agents.py`, `tests/test_jobs.py`.
- Smoke: `uv run python scripts/smoke_test.py`.

## Konfigurácia (env, prefix `AUTOMA_`)
- `SQLITE_URL` (default `sqlite:///./automa.db`)
- `SECRET_KEY`, `JWT_ALGORITHM` (default `HS256`), `ACCESS_TOKEN_EXPIRE_MINUTES` (default `60`)
- `ADMIN_EMAIL` (default `admin@example.com`), `ADMIN_PASSWORD` (default `admin`)
- `CORS_ORIGINS` (zoznam)

## API rýchly štart
1) Získaj token: `POST /api/v1/auth/token` (form: username, password)
2) Autorizácia: `Authorization: Bearer <token>`
3) Správa: `/api/v1/agents`, `/api/v1/scripts`, `/api/v1/jobs`

## Migrácie (Alembic)
- Upgrade: `uv run alembic upgrade head`
- Nová revízia: `uv run alembic revision --autogenerate -m "popis"`
- Pozn.: baseline je prázdny; tabuľky vytvorí app pri štarte (SQLModel).
