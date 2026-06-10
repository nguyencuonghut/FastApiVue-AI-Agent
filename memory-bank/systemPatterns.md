# System Patterns

## Agent Workflow Pattern

This repository uses a two-layer memory pattern:

1. `AGENTS.md` for always-loaded startup instructions
2. `memory-bank/` for durable, human-readable project context

## Memory Pattern

The chosen memory design is adapted from `axiomhq/agent-memory`:

1. capture durable learning
2. consolidate into structured memory
3. surface hot memory into startup instructions

## Documentation Pattern

If code and docs disagree:

1. verify with code or commands
2. fix the docs
3. record any recurring mismatch as a bug pattern

## Theme Consistency Pattern

Frontend theme must be centralized.

Use shared semantic tokens/classes for:

- button
- menu/sidebar
- topbar/header
- datatable
- form input
- dialog
- notification

Dark/light mode must change the whole application consistently. Page-level color overrides are only allowed when they are backed by reusable semantic tokens.

## Responsive UI Pattern

Frontend layout must be responsive by default.

Use shared responsive rules for:

- sidebar/menu behavior
- topbar actions
- page spacing
- card grids
- forms
- datatable wrappers
- dialog sizing

Do not rely on page-by-page fixes for mobile. Responsive behavior should come from centralized layout/component styles and tested breakpoints.

## Typography Pattern

Frontend typography is centralized.

Use one shared body font family across the application: `Be Vietnam Pro`.

Font changes belong in the centralized style layer, not in page-level or component-level overrides.

## Time Handling Pattern

Application-facing time behavior must be explicit.

1. treat `Asia/Ho_Chi_Minh` (`GMT+7`) as the default business timezone
2. distinguish `date` from `datetime` in API contracts and UI forms
3. store and transmit datetimes with explicit timezone/offset rules
4. convert display values intentionally instead of relying on runtime defaults
5. verify date-range filters against start-of-day and end-of-day boundaries in the target timezone

## Auth Strategy Pattern

Phase 2 auth uses a hybrid browser-first token model.

1. access token is short-lived and sent via `Authorization Bearer`
2. refresh token is longer-lived and stored in an `httpOnly` cookie
3. frontend keeps access token in memory only
4. refresh token must not be exposed as raw JSON payload or stored raw in the database
5. auth bootstrap should attempt refresh before treating the user as anonymous

## Enterprise Data Pattern

Large data flows must be server-driven.

DataTable implementations use server-side pagination, filtering, and sorting. Frontend state stores query/selection state, not entire large datasets.

Import/export flows use asynchronous jobs:

1. upload or create request
2. create job
3. process by worker in chunks
4. expose progress/status
5. write output or error report to MinIO
6. audit the operation

## Production Readiness Pattern

Production readiness is part of the architecture, not a deployment afterthought.

Every production service must have:

- observability: logs, metrics, traces, request/correlation id
- backup/restore: scheduled backups, retention, restore drill
- secret management: environment-specific secret source, no committed secrets
- SLO: explicit availability, latency, error-rate targets
- compliance gates: lint, tests, security scans, image scans, migration checks, backup health

## Backend Scaffold Pattern

The backend uses a thin-entrypoint FastAPI structure:

1. `app/main.py` exposes the ASGI app
2. `app/core/application.py` owns app creation and middleware wiring
3. `app/api/router.py` and `app/api/v1/router.py` compose routers by version
4. `app/core/config.py` owns typed settings
5. `app/db/session.py` owns SQLAlchemy async engine/session factory
6. `app/storage/minio.py` owns MinIO client construction

Health endpoints exist at both `/health` and `/api/v1/health`.

Request correlation is centralized through middleware, not repeated inside route handlers.

## Frontend Scaffold Pattern

The frontend uses a thin-SFC and external-logic pattern:

1. `src/main.ts` wires Pinia, Router, PrimeVue, and theme initialization
2. `src/router/index.ts` owns route registration
3. `src/stores/` owns cross-page UI state such as theme and layout
4. `src/composables/` owns page logic and validation orchestration
5. `src/layouts/` owns the admin shell
6. `src/components/` owns reusable view blocks
7. `src/styles/` is the source of truth for tokens, base styles, vendors, layouts, components, and pages
8. `src/styles/main.scss` is the single style entrypoint imported by `src/main.ts`

Vue SFCs must not use style blocks. Keep styles in the centralized `src/styles/**/*.scss` tree and rely on explicit class namespaces per component/layout/page.

The frontend lint pipeline should fail if any `.vue` file contains a `<style>` block.

Vitest unit tests must not scan Playwright specs. Keep `tests/unit` and `tests/e2e` separated and constrain Vitest `include` patterns explicitly.

PrimeVue is configured with a custom preset and `darkModeSelector` bound to `.app-dark` so manual theme switching stays consistent across shared components.

Admin shell should follow a Sakai-like separation of concerns:

1. topbar owns global controls such as sidebar toggle, theme mode, notifications, profile, and logout
2. page context such as section label and page title should live in a dedicated page-header area below the topbar, not inside the topbar itself
3. collapsed desktop sidebar must switch nav to icon-first rendering and hide text labels instead of letting them overflow
4. mobile sidebar must not stay in normal page flow; it should open as an off-canvas overlay with a backdrop so the topbar and content remain vertically ordered
5. footer belongs to the shared admin shell, not to individual pages, so global metadata such as product identity and default timezone stay consistent across the app

## Docker Dev Pattern

Docker dev should optimize for repeatable local startup and low-friction rebuilds:

1. keep dedicated Dockerfiles under `docker/`
2. use a root `.dockerignore` so build context excludes docs, memory, vendor mirrors, caches, and local artifacts
3. keep source bind-mounted for backend/frontend dev loops
4. persist `.venv` and `node_modules` in named volumes so bind mounts do not erase installed dependencies
5. expose infra ports through environment-overridable host-port variables because `5432`, `9000`, and `9001` frequently collide with other local services
6. verify service readiness with healthchecks and container-internal HTTP calls when host localhost access is constrained by the agent environment

## Docker Production Pattern

Docker production should differ from dev in explicit, auditable ways:

1. use multi-stage Dockerfiles with separate `dev` and `prod` targets
2. do not mount source code in production compose
3. run backend with a non-reload server command
4. build frontend static assets ahead of runtime instead of serving Vite dev server
5. place reverse-proxy routing in `docker/nginx/` and keep `/api/*` to backend, `/` to frontend
6. do not publish Postgres or MinIO ports publicly in production scaffold unless a later requirement explicitly needs it
7. keep the public entrypoint isolated to a single proxy port that is environment-overridable

## Docker Test Pattern

Docker test should separate runner responsibilities:

1. keep `backend-test`, `frontend-test`, and `e2e-test` as explicit services
2. give test infra its own Postgres/MinIO services and volumes
3. set `PYTHONPATH=/app` explicitly for backend test containers when the package layout requires it
4. point browser E2E at internal service DNS names like `frontend-e2e` and `backend-e2e`
5. prefer a dedicated Docker build path for Playwright dependencies instead of relying on host-installed browsers
6. when browser tests hit a Vite dev server through Docker DNS, explicitly allow the service hostname in `server.allowedHosts`

## Quality Gate Pattern

The root `Makefile` is the canonical developer entrypoint for pre-commit checks:

1. `make backend-check` runs backend lint, format-check, typecheck, tests, and Bandit
2. `make frontend-check` runs frontend lint, format-check, typecheck, and unit tests
3. `make frontend-test-e2e` is a separate local browser gate because host socket policies may differ by environment
4. `make docker-test-e2e` is the reliable browser E2E gate for sandboxed or CI-like environments
5. `make check` should stay stable and fast enough for routine local validation
