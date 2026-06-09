# Tech Context

## Verified

- Shell environment: `bash`
- Project memory system: `vendor/agent-memory` concepts plus `memory-bank/`
- Local agent instructions entrypoint: `AGENTS.md`
- Local skills directory: `.agents/skills/`

## Planned Stack

- Backend: FastAPI `0.136.3`, Python `3.12` or `3.13`, Pydantic v2, SQLAlchemy, Alembic
- Infrastructure: Docker dev/prod/test, Docker Compose, Postgres, MinIO, production reverse proxy, Redis or compatible broker/cache if background jobs require it
- Frontend: Vue 3, TypeScript, Vite, Pinia, PrimeVue v4, PrimeIcons
- Admin UI reference: Sakai Vue
- Form validation: VeeValidate + Zod
- Backend quality tools: Ruff, mypy or pyright, pytest, pytest-asyncio, pytest-cov, testcontainers or Docker Compose test profile, Bandit
- Frontend quality tools: ESLint, Prettier, vue-tsc, Vitest, Vue Test Utils, Playwright, MSW or API mock layer
- Enterprise features: async User import/export jobs, large DataTable performance, heavy file import/export handling, RBAC, audit logging, rate limiting, dependency/container scanning
- Production readiness: OpenTelemetry, structured logs, metrics/tracing, backup/restore, secret management, SLO, compliance gates

## Unverified

- Actual application source implementation has not been created yet.

## Important Note

The stack above is the approved design direction, not yet implemented source code.

Any agent that later creates or verifies the real stack from code should update this file immediately.
