 # Repository Guidelines

 ## Project Structure & Module Organization
 - `main.py`: CLI entry point; keep top-level logic minimal.
 - `pyproject.toml`: Project metadata and Python version (>= 3.14).
 - `README.md`: Short project overview and usage notes.
 - Optional as the code grows: place modules under `automa/` and tests under `tests/`.

 ## Build, Test, and Development Commands
 - Run app: `python main.py`
 - Lint (optional): `ruff .` — static analysis if Ruff is installed.
 - Format (optional): `black .` — auto-format if Black is installed.
 - Tests (when added): `pytest -q` — run unit tests in `tests/`.

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
