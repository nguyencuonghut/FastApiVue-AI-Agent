# Backend

FastAPI backend scaffold cho `FastApiVueBoilerplate`.

## Lệnh chính

```bash
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run bandit -r app
```
