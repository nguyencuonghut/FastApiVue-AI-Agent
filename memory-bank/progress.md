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
- Completed Phase 2 Step 4 scaffold at code level: added backend permission resolver helpers, `require_permission(...)`, eager loading of `roles -> permissions` for current-user/auth flows, and RBAC core tests
- Completed Phase 2 Step 5 scaffold at code level: added auth request/response schemas, `/api/v1/auth/login|refresh|logout|me` routes, refresh-cookie handling, and auth API contract tests
- Completed Phase 2 Step 6 scaffold at code level: added baseline auth seed constants, idempotent auth/RBAC seed service, seed-related settings/env vars, `backend/scripts/seed_auth_rbac.py`, and `Makefile`/README wiring for initial admin/bootstrap data
- Completed Phase 2 Step 7 scaffold at code level: added frontend auth API client, shared HTTP helper, auth and permission stores, router guards, login page, forbidden page, logout UI, and verified anonymous redirect to login through Docker Playwright E2E
- Hardened the frontend API boundary for auth: split backend DTOs from frontend domain models and added `auth.mappers.ts` so future backend contract changes stay localized to the API layer
- Completed Phase 2 Step 8 scaffold at code level: added `AuditLogService`, wired auth routes to emit audit events for login success/failure, session refresh, and logout, and re-verified backend `pytest` + `ruff` + `mypy`
- Completed the remaining Step 8 scope from the Phase 2 plan: added minimal admin mutation endpoints for `create user` and `update user roles`, protected them with `require_permission(...)`, emitted audit events for both, and re-verified backend `pytest` + `ruff` + `mypy`
- Completed full Users CRUD interface (listing, pagination, filter, search, sorting, details, creation, updates, and deletion) along with the system Roles list endpoint, and verified with passing frontend lint, typecheck, unit tests, and API contract unit tests.
- Completed Phase 4 Storage & Audit integration: implemented database `File` ORM model, Alembic table migration, lifespan auto-bootstrap bucket setup, file services, files API controllers (with FastAPI streaming download proxy), audit logging triggers, frontend types/mappers/api client, vue composables, responsive FilesPage with FileUpload interface, and verified with passing backend unit/contract tests and frontend checks.
- Re-verified on 10/06/2026 that Phases 2, 3, and 4 are complete against the current design doc scope. Backend `pytest`, `ruff`, and `mypy` pass; frontend `typecheck`, `lint`, `test:unit`, and `build` pass.
- Fixed Docker dev startup regression on 10/06/2026: removed the default Redis host-port binding from `docker-compose.yml`, so `docker compose up --build` no longer fails when local port `6379` is already occupied.
- Fixed frontend auth login regression on 10/06/2026: added backend CORS middleware and a preflight regression test so browser `OPTIONS /api/v1/auth/login` no longer fails with `405`.
- Fixed dev auth bootstrap/runtime on 10/06/2026: corrected Alembic Docker path + async env, fixed duplicate enum creation in the first migration, fixed async relationship initialization in auth seed, fixed enum value persistence for `UserStatus`, ran migrations successfully, and seeded the local admin account.
- Implemented user profile fields (`full_name` and `avatar_url`) on 11/06/2026: updated initial Alembic migration directly, mapped attributes in User ORM model, exposed them through backend Pydantic schemas (UserResponse, CurrentUserResponse), updated UserAdminService, populated them in auth endpoints, and wired frontend types, normalizer mappers, useUsersPage composable form states/validation, and UsersPage DataTable columns and dialog fields.
- Audited required-field markers on 11/06/2026 and extended the red-asterisk convention beyond Login/Users to Roles, Files upload, and the dashboard Quick Filter form. Project rules and design docs now treat the marker as a mandatory form UX contract.
- Replaced manual avatar URL entry in Users management with image upload flow on 11/06/2026: added backend `/api/v1/users/avatar-upload`, reused file storage + MinIO, updated Users create/edit dialogs to upload images instead of typing links, and verified backend route tests in-container plus frontend lint/typecheck/unit/build.
- Fixed avatar preview URL regression on 11/06/2026 by switching backend file/avatar/job payloads from absolute URLs to relative `/api/v1/...` paths, preventing browser `ERR_NAME_NOT_RESOLVED` when the backend runs behind Docker/Vite proxy hostnames.
- Refined the shared topbar on 11/06/2026: removed inline email/logout controls, added avatar-trigger dropdown account menu, and introduced a minimal authenticated `/profile` page so the new `Hồ sơ` action has a valid destination.
- Fixed topbar avatar stale-state on 11/06/2026: when Users edit saves the currently logged-in account, the flow now refreshes `authStore.currentUser` immediately so the shell avatar updates without page reload.

## Open

- Start `Phase 5: Hardening`
- Optionally install Bun and run the upstream `agent-memory` CLI locally
