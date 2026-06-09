# Tech Context

## Verified

- Shell environment: `bash`
- Project memory system: `vendor/agent-memory` concepts plus `memory-bank/`
- Local agent instructions entrypoint: `AGENTS.md`
- Local skills directory: `.agents/skills/`
- Backend scaffold exists in `backend/`
- Backend package manager and runner: `uv`
- Verified backend dependency set from `backend/pyproject.toml` and `backend/uv.lock`
- Verified backend app entrypoint: `backend/app/main.py`
- Verified backend framework/tooling: FastAPI `0.136.3`, SQLAlchemy `2.0.50`, Alembic `1.18.4`, Pydantic Settings `2.14.1`, MinIO `7.2.20`, pytest `9.0.3`, pytest-asyncio `1.4.0`, Ruff `0.15.16`, mypy `1.20.2`
- Verified backend checks run successfully on 2026-06-09: `uv run pytest`, `uv run ruff check .`, `uv run mypy .`

## Planned Stack

- Backend: FastAPI `0.136.3`, Python `3.12` or `3.13` target, Pydantic v2, SQLAlchemy, Alembic
- Infrastructure: Docker dev/prod/test, Docker Compose, Postgres, MinIO, production reverse proxy, Redis or compatible broker/cache if background jobs require it
- Frontend: Vue 3, TypeScript, Vite, Pinia, PrimeVue v4, PrimeIcons
- Admin UI reference: Sakai Vue
- Form validation: VeeValidate + Zod
- Backend quality tools: Ruff, mypy or pyright, pytest, pytest-asyncio, pytest-cov, testcontainers or Docker Compose test profile, Bandit
- Frontend quality tools: ESLint, Prettier, vue-tsc, Vitest, Vue Test Utils, Playwright, MSW or API mock layer
- Enterprise features: async User import/export jobs, large DataTable performance, heavy file import/export handling, RBAC, audit logging, rate limiting, dependency/container scanning
- Production readiness: OpenTelemetry, structured logs, metrics/tracing, backup/restore, secret management, SLO, compliance gates

## Unverified

- Frontend source implementation has not been created yet.
- Docker Compose dev/prod/test files have not been created yet.
- Database connectivity and MinIO connectivity are scaffolded but not exercised against running services yet.

## Important Note

The backend portion is now partially implemented and verified. Frontend and container orchestration remain design-stage only.

Any agent that later creates or verifies the real stack from code should update this file immediately.
