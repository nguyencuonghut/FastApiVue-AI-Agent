# Backend

FastAPI backend scaffold cho `FastApiVueBoilerplate`.

## Lệnh chính

```bash
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
uv run python scripts/seed_auth_rbac.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run bandit -r app
XDG_CACHE_HOME=/tmp/.cache uv run pip-audit
```
