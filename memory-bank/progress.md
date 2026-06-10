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
- Fixed the mobile admin shell: moved small-screen sidebar behavior to an off-canvas overlay with backdrop, added viewport-aware layout state, tightened mobile spacing, and re-verified Docker browser E2E
- Fixed mobile shell width drift: topbar, page header, content wrapper, and dashboard cards now use symmetric mobile gutters with full-width constraints and clipped horizontal overflow
- Added system-wide typography and time baseline: `Be Vietnam Pro` is the default UI font, `.env.example` now carries `APP_TIMEZONE` and `VITE_APP_TIMEZONE`, and project rules now require explicit `Asia/Ho_Chi_Minh` time handling
- Fixed dashboard form overflow: PrimeVue `Owner Email` input in `Quick Filter Form` is now constrained correctly inside the card on desktop/mobile
- Added a shared admin-shell footer in `AdminLayout` with consistent product metadata and timezone display sourced from `VITE_APP_TIMEZONE`
- Added `docs/phase-2-auth-rbac-implementation-plan.md` with scope, deliverables, rollout order, acceptance criteria, risks, and test matrix for Phase 2
- Closed Phase 2 Step 1 auth strategy: added `docs/phase-2-auth-strategy-decision.md`, updated design/plan docs, and introduced hybrid auth config baseline in `.env.example` and backend settings
- Completed Phase 2 Step 2 scaffold at code level: added auth/RBAC ORM models, metadata registration, a first Alembic revision, and a schema metadata test for users/roles/permissions/refresh_tokens/audit_logs
- Completed Phase 2 Step 3 scaffold at code level: added password hashing, JWT access-token issue/decode, refresh-token issue/refresh/revoke flow, current-user dependency, and auth core tests under `backend/app/auth/`

## Open

- Start recording real bug history
- Optionally install Bun and run the upstream `agent-memory` CLI locally
