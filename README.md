## Run with uv

- Pin Python: `uv python pin 3.13`
- Install deps: `uv sync`
- Start API: `uv run uvicorn automa.api.app:app --reload`
- Tests: `uv run pytest -q`

Health check: visit `http://localhost:8000/api/v1/health`.
