# Active Context

## Current Focus

The repository has been prepared with:

1. local skills from `mattpocock/skills`
2. a project-local memory workflow based on `axiomhq/agent-memory`
3. mandatory startup rules in `AGENTS.md`
4. a fullstack boilerplate design targeting FastAPI, Docker, MinIO, Postgres, Vue 3, TypeScript, Pinia, PrimeVue v4, and Sakai-inspired admin UI
5. enterprise requirements for User import/export, large DataTable performance, heavy file processing, and security baseline
6. production readiness requirements for observability, backup/restore, secret management, SLO, and compliance gates
7. a verified backend scaffold in `backend/` with FastAPI, typed settings, request-id middleware, SQLAlchemy async session skeleton, MinIO client scaffold, Alembic stub, and health endpoint tests
8. a verified frontend scaffold in `frontend/` with Vue 3, TypeScript, Vite, Vue Router, Pinia, PrimeVue v4, VeeValidate + Zod, shared dark/light theme tokens, unit tests, Playwright smoke test, and successful production build
9. a repository rule that Vue SFC must not use style blocks, with automatic lint enforcement in `frontend/scripts/check-no-scoped-style.mjs`
10. a centralized frontend style architecture in `frontend/src/styles/**/*.scss` covering tokens, base, vendors, layouts, components, and pages
11. a verified Docker dev scaffold with `docker-compose.yml`, backend/frontend Dockerfiles, Postgres, MinIO, customizable host ports, and reduced build context via root `.dockerignore`
12. a verified Docker production scaffold with multi-stage backend/frontend Dockerfiles, frontend static build, Nginx reverse proxy config, and `docker-compose.prod.yml` without source mounts or public Postgres/MinIO ports
13. a fully verified Docker test scaffold exists with `docker-compose.test.yml`, isolated test data volumes, dedicated backend/frontend/e2e runners, and a Playwright-specific Docker path that passes after allowing the `frontend-e2e` Vite hostname
14. a root `Makefile` now provides the canonical local and Docker quality-gate commands for backend, frontend, aggregate checks, and browser E2E
15. mobile responsive behavior is now a mandatory frontend requirement alongside dark/light consistency, not an optional later enhancement
16. the admin shell now uses a responsive split behavior: collapsed icon-first sidebar on desktop and off-canvas sidebar with backdrop on mobile so topbar/page-header/content keep Sakai-like ordering
17. typography and time handling are now explicit system constraints: UI uses `Be Vietnam Pro`, and business-facing date/time behavior defaults to `Asia/Ho_Chi_Minh` (`GMT+7`)
18. a dedicated implementation plan now exists for `Phase 2: Auth + RBAC`, covering schema, auth core, permission guards, seed data, frontend auth foundation, audit log, and test milestones
19. Phase 2 auth strategy is now closed: short-lived Bearer access token plus `httpOnly` refresh cookie, with config baseline already added to `.env.example` and backend settings
20. Phase 2 database foundation is now scaffolded in code: auth/RBAC ORM models and a first Alembic revision exist for `users`, `roles`, `permissions`, `user_roles`, `role_permissions`, `refresh_tokens`, and `audit_logs`
21. Phase 2 auth core service is now scaffolded in code: password hashing, JWT access-token issue/decode, refresh-token issue/refresh/revoke, and `get_current_user` dependency exist under `backend/app/auth/`
22. Phase 2 RBAC core is now scaffolded in code: permission resolver helpers and `require_permission(...)` exist, and current-user fetches eager-load `roles -> permissions`
23. Phase 2 auth API is now scaffolded in code: `/api/v1/auth/login`, `/refresh`, `/logout`, and `/me` exist with hybrid cookie+Bearer contract and response schemas
24. Phase 2 seed-data foundation is now scaffolded in code: base permission codes, `admin`/`user` roles, initial admin-user bootstrap service, seed script, and seed-related env config now exist under `backend/app/auth/`, `backend/app/services/`, and `backend/scripts/`
25. Phase 2 frontend auth foundation is now scaffolded in code: `auth.api`, shared `http` client, `auth` and `permission` stores, router guards, login page, forbidden page, logout UI, and anonymous-to-login bootstrap behavior now exist under `frontend/src/`
26. Frontend auth API boundary is now hardened: backend DTOs are separated from frontend domain models through `auth.mappers.ts`, so auth contract drift should stay localized to `src/api` and type files

## Next Useful Steps

1. Start `Phase 2` Step 8 audit-log foundation for login/logout and admin auth/RBAC changes.
2. Populate bug history when the first business-logic defects are fixed.
3. Keep `techContext.md` and `projectRules.md` synchronized with real project discoveries.
