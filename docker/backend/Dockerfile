FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock backend/README.md ./
RUN uv sync

COPY backend /app

EXPOSE 8000

CMD ["sh", "-lc", "uv sync && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
