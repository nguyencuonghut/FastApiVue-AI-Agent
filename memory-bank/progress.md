# Progress

## Completed

- Installed local skills into `.agents/skills/`
- Added root `AGENTS.md`
- Mirrored `axiomhq/agent-memory` into `vendor/agent-memory/`
- Added project-local `memory-bank/`
- Added project-local `.agent-memory/` layout
- Added docs for memory integration and agent rules
- Added fullstack boilerplate design doc in `docs/fullstack-boilerplate-design.md`
- Added requirements for Docker dev/prod/test and automatic test frameworks for backend/frontend
- Added system-wide dark/light theme consistency requirement for buttons, menus, headers, data tables, form inputs, and shared UI components
- Added a mandatory mobile-responsive requirement for frontend layout and shared UI
- Upgraded design requirements to enterprise level: User import/export, large DataTable performance, heavy file import/export jobs, and stronger security baseline
- Added production readiness requirements: observability, backup/restore, secret management, SLO, and compliance gates
- Added Phase 1 scaffold implementation plan in `docs/phase-1-scaffold-implementation-plan.md`
- Completed Phase 1 Step 1 repository preparation: `.gitignore`, `README.md`, `.env.example`, and vendor Git isolation
- Completed Phase 1 Step 2 backend scaffold: `backend/` app package, FastAPI `0.136.3`, typed settings, request-id middleware, SQLAlchemy async session skeleton, MinIO client scaffold, Alembic stub, `uv.lock`, and verified `pytest` + `ruff` + `mypy`
- Completed Phase 1 Step 3 frontend scaffold: `frontend/` app package, Vue `3.5.x`, Vite `8`, Router, Pinia, PrimeVue `4.5.5`, VeeValidate `4.15.1`, Zod, shared dark/light token layer, unit tests, Playwright smoke test, and verified `typecheck` + `lint` + `build`
- Tightened frontend implementation rule: no `scoped style` in Vue SFC, migrated Step 3 files off `scoped`, and added an automatic lint guard via `frontend/scripts/check-no-scoped-style.mjs`
- Refactored frontend styles into centralized `src/styles/**/*.scss`, removed all `<style>` blocks from Vue SFC files, and verified lint/test/build with Sass enabled
- Completed Phase 1 Step 4 Docker dev: added `docker-compose.yml`, backend/frontend Dockerfiles, root `.dockerignore`, customizable host port mapping, verified container health for backend/frontend/postgres/minio, and verified backend/frontend HTTP responses from inside containers
- Completed Phase 1 Step 5 Docker production: converted backend/frontend Dockerfiles to multi-stage `dev`/`prod`, added `docker-compose.prod.yml`, added Nginx reverse-proxy config, ensured production compose does not mount source code or expose Postgres/MinIO publicly, and verified `docker compose -f docker-compose.prod.yml config` plus production image builds
- Completed Phase 1 Step 6 Docker test profile: added `docker-compose.test.yml`, isolated test Postgres/MinIO volumes, verified `backend-test`, `frontend-test`, and `e2e-test`, and fixed Vite host allowlisting for Docker browser tests
- Completed Phase 1 Step 7 Quality gates: added a root `Makefile` with canonical backend/frontend/local/Docker commands, documented the workflow in `README.md`, and verified `make check` plus Docker browser E2E

## Open

- Start recording real bug history
- Optionally install Bun and run the upstream `agent-memory` CLI locally
