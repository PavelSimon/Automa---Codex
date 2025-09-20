 # Repository Guidelines

 ## Project Structure & Module Organization
 - `main.py`: CLI entry point; keep top-level logic minimal.
 - `pyproject.toml`: Project metadata and Python version (>= 3.14).
 - `README.md`: Short project overview and usage notes.
 - Optional as the code grows: place modules under `automa/` and tests under `tests/`.

 ## Build, Test, and Development Commands (uv)
 - Install deps: `uv sync` (respects `pyproject.toml`).
 - Pin Python: `uv python pin 3.13` (one-time, if needed).
 - Run app: `uv run uvicorn automa.api.app:app --reload --port 7999`.
 - Tests: `uv run pytest -q` — unit tests in `tests/`.
 - Migrations: `uv run alembic upgrade head`; new: `uv run alembic revision --autogenerate -m "msg"`.
 - Lint/Format (optional): `uv run ruff .`, `uv run black .` if tools are added.

 ## Coding Style & Naming Conventions
 - Indentation: 4 spaces; line length ≤ 100 chars.
 - Style: Follow PEP 8; docstrings per PEP 257 for public functions/classes.
 - Naming: `lower_snake_case` for functions/variables, `UpperCamelCase` for classes, `UPPER_SNAKE_CASE` for constants. Modules/packages use `lower_snake_case`.
 - Imports: standard lib → third-party → local, separated by blank lines.

 ## Testing Guidelines
 - Framework: pytest. Tests live in `tests/` and follow `test_*.py`.
 - Included: `tests/test_health.py`, `tests/test_auth_and_agents.py`.
 - Run: `pytest -q` (ensure venv active). Aim ≥ 80% coverage on new code.

 ## Commit & Pull Request Guidelines
 - Commits: Use Conventional Commits, e.g., `feat: add task runner`, `fix: handle empty input`.
 - Scope: small, focused commits with imperative subject; include rationale in the body if non-trivial.
 - Branches: `feature/<short-topic>`, `fix/<issue-id>`, `chore/...`.
 - PRs: clear description, linked issues (e.g., `Closes #12`), steps to test locally, and sample output for CLI changes.

 ## Security & Configuration Tips
 - Do not commit secrets or tokens. Prefer environment variables for config (e.g., `APP_MODE=dev`).
 - Keep new dependencies minimal; update `pyproject.toml` when adding any and justify in the PR.
