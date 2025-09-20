## Run with uv

- Pin Python: `uv python pin 3.13`
- Install deps: `uv sync`
- Start API: `uv run uvicorn automa.api.app:app --reload --port 7999`
- Tests: `uv run pytest -q`

Health check: visit `http://localhost:7999/api/v1/health`.
