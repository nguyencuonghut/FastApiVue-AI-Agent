FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

FROM base AS dev

COPY backend/pyproject.toml backend/uv.lock backend/README.md ./
RUN uv sync

COPY backend /app

EXPOSE 8000

CMD ["sh", "-lc", "uv sync && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]

FROM base AS prod

COPY backend/pyproject.toml backend/uv.lock backend/README.md ./
RUN uv sync --frozen --no-dev

COPY backend /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
