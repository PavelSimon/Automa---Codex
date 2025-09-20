# Postup realizácie (Python 3.13)

## 1) Spresnenie požiadaviek
- Vymenovať typy úloh (spracovanie dát, emailing, scraping, monitoring) a SLA.
- Definovať role (admin, user), požiadavky na audit, logging a plánovanie.

## 2) Technológie a verzovanie
- Backend: FastAPI (async, API-first), Python 3.13.
- DB: SQLite na MVP, príprava na PostgreSQL.
- Plánovanie: APScheduler (jednoduchšie MVP než Celery/Redis).
- Autentifikácia: OAuth2 password flow + JWT (email/heslo).
- Sandbox: spúšťanie úloh v Docker kontajneroch (Docker Desktop/Podman).
- Logovanie/Audit: štruktúrované JSON logy + tabuľka v DB.

## 3) Architektúra a štruktúra projektu
```
automa/
  api/          # FastAPI routery (agents, jobs, scripts, users, auth)
  core/         # config, security (JWT), deps, logging
  domain/       # modely (SQLModel/SQLAlchemy), služby
  scheduler/    # APScheduler integrácia, spúšťač jobov
  sandbox/      # adaptér pre Docker spúšťanie skriptov/agentov
  plugins/      # voliteľné moduly/rozšírenia (entrypoint alebo dynamické načítanie)
  web/          # jednoduchý HTML/JS dashboard (MVP)
tests/
```

## 4) Implementačné kroky MVP
1. Inicializácia FastAPI, konfigurácia (pydantic settings), štruktúra adresárov.
2. Modely: User, Agent, Script, Job, AuditLog (SQLModel/SQLAlchemy + SQLite).
3. Migrácie: Alembic (alebo jednoduchá init schema pre MVP).
4. Autentifikácia: registrácia/prihlásenie, JWT, role (admin/user).
5. API: CRUD pre Agents/Scripts, vytváranie Jobov (ad‑hoc aj plánovaných).
6. Scheduler: APScheduler (cron/interval/date), persistencia jobov v DB.
7. Sandbox: docker run s obmedzeniami (read‑only FS, CPU/RAM limity, sieť podľa potreby).
8. Logging/Audit: middleware + service, zápis akcií (kto/čo/kedy/status) do DB a JSON logu.
9. Web UI: základny dashboard (prehľad agentov, jobov, logov) cez jednoduché šablóny/JS.

## 5) Bezpečnosť a rozšíriteľnosť
- Politiky práv podľa role, validácia vstupov, rate‑limit (reverse proxy) a CORS.
- Pluginy: definovať rozhranie (Protocol/ABC) a naming `plugins.<názov>.plugin`.
- API: verzovanie `/api/v1`, OpenAPI schema, token-permissions.

## 6) Lokálne spustenie a príkazy (uv)
- Požadovaná verzia: Python 3.13 (`uv python pin 3.13`).
- Inštalácia závislostí: `uv sync` (čerpá z `pyproject.toml`).
- Spustenie API: `uv run uvicorn automa.api.app:app --reload`.
- Testy: `uv run pytest -q` (umiestniť do `tests/`, `test_*.py`).

## 6b) Testovanie (MVP)
- Pridané testy: `tests/test_health.py`, `tests/test_auth_and_agents.py`.
- Pokrytie: základné overenie health checku, získania JWT tokenu a CRUD nad agentmi.
- Spustenie: `uv run pytest -q`.

## 7) Nasadenie
- Lokálne/LAN: Uvicorn/Gunicorn + reverse proxy (Nginx/Caddy), perzistentná DB, Docker daemon.
- Zálohy DB a logov, rotácia logov, periodické audity.

## 8) Migrácie schémy (Alembic)
- Konfigurácia: `alembic.ini`, priečinok `alembic/` (baseline rev `0001_baseline`).
- Prvé spustenie: tabuľky vytvorí aplikácia (SQLModel). Alembic baseline len označí stav.
- Budúce zmeny: po úprave modelov spustiť `uv run alembic revision --autogenerate -m "<popis>"` a `uv run alembic upgrade head`.
- URL DB sa berie z `AUTOMA_SQLITE_URL` alebo default `sqlite:///./automa.db`.
