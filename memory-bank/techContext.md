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
- Frontend scaffold exists in `frontend/`
- Frontend package manager and runner: `npm`
- Verified frontend dependency set from `frontend/package.json` and `frontend/package-lock.json`
- Verified frontend app entrypoint: `frontend/src/main.ts`
- Verified frontend framework/tooling: Vue `3.5.34`, Vite `8.0.16`, Vue Router `5.1.0`, Pinia `3.0.4`, PrimeVue `4.5.5`, PrimeIcons `7.0.0`, VeeValidate `4.15.1`, Zod `3.25.76`, ESLint `10.4.1`, Prettier `3.8.3`, Vitest `4.1.8`, Vue Test Utils `2.4.11`, Playwright `1.60.0`
- Verified frontend checks run successfully on 2026-06-09: `npm run typecheck`, `npm run lint`, `npm run test:unit`, `npm run test:e2e`, `npm run build`
- Verified frontend guardrail: `npm run lint` calls `frontend/scripts/check-no-scoped-style.mjs` to reject any Vue SFC using `<style scoped>`

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

- Docker Compose dev/prod/test files have not been created yet.
- Database connectivity and MinIO connectivity are scaffolded but not exercised against running services yet.
- Frontend runtime integration to a live backend endpoint has not been exercised yet.

## Important Note

Backend and frontend scaffolds are now implemented and verified. Container orchestration and live service integration remain the next major gap.

Any agent that later creates or verifies the real stack from code should update this file immediately.
