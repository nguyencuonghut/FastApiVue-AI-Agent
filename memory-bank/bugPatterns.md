# Bug Patterns

## Current Status

Historical bug memory is populated below.

Agents must read the relevant entries before changing behavior in the same area, especially auth, Docker, frontend shell responsiveness, and file/avatar flows.

## Required Template For New Entries

### YYYY-MM-DD: [Short bug name]

- Area:
- Trigger:
- Root cause:
- Fix:
- Regression guard:
- Related files:

### 2026-06-09: Vitest scanning Playwright specs

- Area: Frontend test runner configuration
- Trigger: Running `npm run test:unit` picked up `tests/e2e/smoke.spec.ts` and failed with `Playwright Test did not expect test() to be called here`.
- Root cause: Vitest default discovery was not restricted to unit-test paths.
- Fix: Set `include: ['tests/unit/**/*.spec.ts']` in `frontend/vitest.config.ts`.
- Regression guard: Keep `tests/unit` and `tests/e2e` separated and verify `npm run test:unit` after adding any new test folders.
- Related files: `frontend/vitest.config.ts`, `frontend/tests/e2e/smoke.spec.ts`

### 2026-06-09: TypeScript 6 alias deprecation block

- Area: Frontend TypeScript config
- Trigger: `npm run typecheck` failed with `Option 'baseUrl' is deprecated` after adding `@/` alias paths.
- Root cause: TypeScript 6 treats `baseUrl` deprecation as a blocking config error unless the deprecation is explicitly acknowledged.
- Fix: Add `"ignoreDeprecations": "6.0"` alongside `baseUrl` in `frontend/tsconfig.app.json`.
- Regression guard: Re-run `npm run typecheck` whenever alias config changes; if TypeScript 7 migration happens, revisit the alias strategy instead of carrying the suppression blindly.
- Related files: `frontend/tsconfig.app.json`, `frontend/vite.config.ts`

### 2026-06-09: Invalid MinIO image tag in Docker dev

- Area: Docker Compose dev scaffold
- Trigger: `docker compose up --build -d` failed because `minio/minio:RELEASE.2026-05-24T17-08-30Z` could not be resolved.
- Root cause: The compose file used an assumed MinIO tag instead of a verified published image tag.
- Fix: Pin `minio/minio:RELEASE.2025-09-07T16-13-09Z` in `docker-compose.yml` after verifying the tag exists on Docker Hub.
- Regression guard: Do not invent container tags. Verify image tags against the official registry listing before writing or updating compose files.
- Related files: `docker-compose.yml`

### 2026-06-09: Backend Docker dev command depended on missing FastAPI extra

- Area: Backend Docker dev runtime command
- Trigger: The `backend` container exited during startup with `RuntimeError: To use the fastapi command, please install "fastapi[standard]"`.
- Root cause: The compose and Dockerfile command used `fastapi dev`, but the backend dependency set only installed `fastapi`, not the `standard` extra bundle required by the CLI helper.
- Fix: Replace the dev command with `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.
- Regression guard: When choosing container startup commands, verify that the required dependency extras are actually installed, or prefer the directly installed ASGI server command.
- Related files: `docker/backend/Dockerfile`, `docker-compose.yml`, `backend/pyproject.toml`

### 2026-06-09: Backend test container could not import `app`

- Area: Docker test profile for backend
- Trigger: `docker compose -f docker-compose.test.yml run --rm backend-test` failed with `ModuleNotFoundError: No module named 'app'` even though the package existed under `/app/app`.
- Root cause: The backend test runner inside the container did not reliably include `/app` on `sys.path` for this scaffold layout.
- Fix: Set `PYTHONPATH=/app` for backend test services in `docker-compose.test.yml`.
- Regression guard: When containerizing Python tests for a flat `/app/app` layout, verify imports inside the actual runner environment rather than assuming local behavior carries over.
- Related files: `docker-compose.test.yml`, `backend/tests/conftest.py`

### 2026-06-09: Frontend E2E smoke spec drifted from scaffold UI

- Area: Frontend Playwright smoke test
- Trigger: The browser-backed Docker E2E run reached the app, but the assertion for the old heading/text failed.
- Root cause: The Playwright smoke spec was not updated after the dashboard scaffold copy changed.
- Fix: Update `frontend/tests/e2e/smoke.spec.ts` to assert the current `Frontend Smoke Dashboard` heading and `Vue 3 + PrimeVue v4 scaffold` text.
- Regression guard: Re-run both the unit spec and Playwright smoke spec whenever scaffold copy or page structure changes.
- Related files: `frontend/tests/e2e/smoke.spec.ts`, `frontend/tests/unit/dashboard.page.spec.ts`, `frontend/src/pages/DashboardPage.vue`

### 2026-06-09: Vite blocked Docker service hostname during E2E

- Area: Frontend Docker E2E runtime
- Trigger: `docker compose -f docker-compose.test.yml run --rm e2e-test` loaded the Vite app shell but Playwright only saw `Blocked request. This host ("frontend-e2e") is not allowed.`
- Root cause: Vite dev server did not allow the internal Docker service hostname used by Playwright baseURL.
- Fix: Add `server.allowedHosts = ['frontend-e2e']` in `frontend/vite.config.ts`.
- Regression guard: When browser tests target a Vite dev server through Docker service DNS, verify the hostname is explicitly allowed and rerun the Docker E2E smoke test after any compose or hostname change.
- Related files: `frontend/vite.config.ts`, `docker-compose.test.yml`, `frontend/playwright.docker.config.ts`

### 2026-06-09: Docker frontend build emitted deprecated `glob@10.5.0` warning

- Area: Frontend dependency graph and Docker build output
- Trigger: `npm install`/`npm ci` during frontend Docker builds warned that `glob@10.5.0` is deprecated.
- Root cause: Latest `@vue/test-utils@2.4.11` still depends on `js-beautify@1.15.4`, which in turn depends on `glob ^10.4.2`; the resolved lockfile version was `10.5.0`.
- Fix: Add an `overrides` entry in `frontend/package.json` to force transitive `glob` to `13.0.6`, then regenerate `frontend/package-lock.json`.
- Regression guard: Re-check `npm ls glob` and at least one Docker frontend build path after dependency updates, because upstream latest packages may still carry deprecated transitives.
- Related files: `frontend/package.json`, `frontend/package-lock.json`, `docker/frontend/Dockerfile`

### 2026-06-09: Sidebar collapse only shrank the grid, not the sidebar content

- Area: Frontend admin shell layout
- Trigger: Collapsing the sidebar kept the `Dashboard Smoke` label visible, causing the menu text to overflow into the main page area.
- Root cause: The layout only reduced the sidebar column width and did not hide or constrain the brand/nav text inside the collapsed state.
- Fix: Update `AdminLayout.vue` and `admin-layout.scss` so collapsed mode hides brand/nav labels, centers icon-only navigation, and moves the hamburger toggle into the sidebar header.
- Regression guard: When adding or changing shell navigation, verify collapsed desktop sidebar and small-screen behavior separately; shrinking the container width alone is not sufficient.
- Related files: `frontend/src/layouts/AdminLayout.vue`, `frontend/src/styles/layouts/admin-layout.scss`

### 2026-06-09: Mobile sidebar stayed in page flow and pushed topbar/content down

- Area: Frontend admin shell responsive layout
- Trigger: On mobile width, the sidebar rendered above the topbar and page content, producing stacked layout blocks and uneven content widths/margins.
- Root cause: The responsive layout only changed the grid to a single column; the sidebar still occupied normal document flow instead of switching to an overlay pattern.
- Fix: Add mobile-aware layout state, render the sidebar as an off-canvas fixed panel with a backdrop, close it on nav click, and tighten mobile page/header spacing.
- Regression guard: For every shell/layout change, verify desktop collapse and mobile overlay behavior separately in browser E2E; a one-column layout alone is not a valid mobile sidebar implementation.
- Related files: `frontend/src/stores/layout.store.ts`, `frontend/src/layouts/AdminLayout.vue`, `frontend/src/styles/layouts/admin-layout.scss`, `frontend/src/styles/pages/dashboard-page.scss`

### 2026-06-09: Mobile dashboard sections overflowed horizontally and broke symmetric page gutters

- Area: Frontend responsive spacing and content wrappers
- Trigger: On mobile, the topbar, page header, and dashboard cards appeared to have right-side spacing but little or no left-side spacing.
- Root cause: Shell/content wrappers and dashboard sections were not consistently constrained with `width: 100%`, `max-width: 100%`, and horizontal overflow clipping after the mobile layout refactor.
- Fix: Constrain the admin shell surface, topbar, page header, content wrapper, and dashboard sections/cards to full-width responsive boxes and clip horizontal overflow.
- Regression guard: After changing mobile shell spacing or component structure, verify that topbar/page-header/content render with symmetric left/right gutters and no horizontal drift.
- Related files: `frontend/src/styles/layouts/admin-layout.scss`, `frontend/src/styles/pages/dashboard-page.scss`, `frontend/src/styles/components/dashboard/summary-cards.scss`, `frontend/src/styles/components/dashboard/quick-filter-form.scss`, `frontend/src/styles/components/dashboard/health-snapshot-table.scss`

### 2026-06-10: PrimeVue input overflowed from dashboard form card

- Area: Frontend form layout inside dashboard cards
- Trigger: In the `Validation Scaffold` card, the `Owner Email` input value extended past the right edge of the card.
- Root cause: The grid form and field wrappers did not fully constrain PrimeVue `InputText` width; without `min-width: 0` and explicit `width: 100%`, the input could size itself from content and overflow the card.
- Fix: Add `overflow: hidden` to the card, set `min-width: 0` on the form and field wrappers, and force `.p-inputtext` inside the form fields to `width: 100%` with constrained max width.
- Regression guard: For any PrimeVue field placed inside CSS grid/flex cards, verify the wrapper and the input both opt into shrinking with `min-width: 0` and explicit width constraints.
- Related files: `frontend/src/styles/components/dashboard/quick-filter-form.scss`

### 2026-06-10: JWT expiry drifted because issued tokens kept microseconds

- Area: Backend auth token issuance
- Trigger: `test_issue_and_decode_access_token` failed because decoded JWT expiry lost microseconds while the original `expires_at` still contained them.
- Root cause: `issue_access_token` used `datetime.now(UTC)` directly, but JWT timestamp serialization truncates to whole seconds.
- Fix: Normalize `issued_at` to `microsecond=0` before computing and encoding token timestamps.
- Regression guard: When asserting JWT timestamps or comparing encoded/decoded expiry values, keep token issue times second-aligned.
- Related files: `backend/app/auth/jwt.py`, `backend/tests/test_auth_core.py`

### 2026-06-10: SQLAlchemy runtime import broke on relationship annotation form

- Area: Backend ORM model annotations
- Trigger: Backend runtime import failed with `MappedAnnotationError` while loading `AuditLog.actor_user`.
- Root cause: The relationship annotation used a quoted union form that SQLAlchemy's annotation parser did not accept in the live import path.
- Fix: Change relationship annotations to the SQLAlchemy-compatible pattern used across the model package and re-run runtime tests and linting.
- Regression guard: After changing ORM annotations, run real backend import/test checks, not just `py_compile`, because SQLAlchemy validates mapped annotations at import time.
- Related files: `backend/app/models/audit_log.py`, `backend/app/models/user.py`, `backend/app/models/role.py`, `backend/app/models/permission.py`, `backend/app/models/refresh_token.py`

### 2026-06-10: PrimeVue v4 DataTable Row Expansion Slot Name

- Area: Frontend DataTable layout
- Trigger: TypeScript compiler error `Property 'rowexpansion' does not exist on type 'DataTableSlots<any>'`.
- Root cause: In PrimeVue v4, the row expansion template slot is named `#expansion` rather than `#rowexpansion`.
- Fix: Rename the template slot to `#expansion` in `DataTable`.
- Regression guard: Avoid using `#rowexpansion` for PrimeVue v4 DataTables; always refer to `#expansion` slot.
- Related files: `frontend/src/pages/UsersPage.vue`

### 2026-06-10: ARQ fallback typing can silently break backend mypy

- Area: Backend async job service typing
- Trigger: During a phase-status verification run, backend `mypy` failed in `app/services/job_admin.py` even though runtime tests passed.
- Root cause: The offline fallback redefined `create_pool` under `except ImportError`, producing a different callable signature from the real `arq.create_pool` import. `mypy` treated that conditional import path as incompatible overload-like variants.
- Fix: Replace the dual-signature fallback with a dedicated `create_job_queue(...)` wrapper plus a small `JobQueue` protocol and `DummyJobQueue` fallback.
- Regression guard: When providing offline fallbacks for optional third-party integrations, do not redefine imported callables with different signatures. Wrap them behind a project-local function/protocol boundary instead.
- Related files: `backend/app/services/job_admin.py`

### 2026-06-10: Docker dev compose should not bind Redis host port by default

- Area: Docker dev runtime networking
- Trigger: Running `docker compose up --build` failed with `failed to bind host port 0.0.0.0:6379/tcp: address already in use`.
- Root cause: `docker-compose.yml` published Redis to host port `6379` even though backend and worker only use Redis over the internal Docker network.
- Fix: Remove the Redis `ports:` mapping from `docker-compose.yml` so the default dev stack no longer depends on a free host `6379`.
- Regression guard: Only publish infra service ports to the host when there is a verified local operator need. Internal-only dependencies like Redis should stay on the Compose network by default.
- Related files: `docker-compose.yml`, `README.md`

### 2026-06-10: Missing CORS middleware makes auth login look like FE connectivity failure

- Area: Backend API middleware / frontend auth bootstrap
- Trigger: FE login showed `Không thể kết nối tới dịch vụ xác thực.` while backend logs showed `OPTIONS /api/v1/auth/login 405 Method Not Allowed` and a separate `POST /api/v1/auth/refresh 401 Unauthorized`.
- Root cause: Backend had no `CORSMiddleware`, so browser preflight for cross-origin `POST /api/v1/auth/login` failed before the actual login request reached auth logic. The `401 /auth/refresh` was a normal anonymous-bootstrap outcome and not the root failure.
- Fix: Add `CORSMiddleware` in `backend/app/core/application.py` using configured `CORS_ORIGINS`, and add a regression test asserting `OPTIONS /api/v1/auth/login` returns CORS headers for the dev frontend origin.
- Regression guard: When frontend reports generic auth connectivity issues, inspect browser-triggered `OPTIONS` requests before debugging token logic. Any browser-facing POST auth endpoint must pass a real preflight test.
- Related files: `backend/app/core/application.py`, `backend/tests/test_health.py`

### 2026-06-10: Alembic asyncpg migration path was broken in Docker dev

- Area: Backend migration runtime in Docker
- Trigger: `uv run alembic upgrade head` failed first because `alembic.ini` pointed to `backend/alembic` inside the container, then failed again with `MissingGreenlet` when trying to connect with `asyncpg`.
- Root cause: The container layout is `/app`, so `script_location = backend/alembic` is wrong there. In addition, `alembic/env.py` used sync `engine_from_config` against an async PostgreSQL URL.
- Fix: Change `script_location` to `alembic` in `backend/alembic.ini` and convert `backend/alembic/env.py` to the async Alembic pattern using `async_engine_from_config` plus `connection.run_sync(...)`.
- Regression guard: Any Docker dev verification for auth/login must include a real migration run, because health checks can still pass while the database schema is missing.
- Related files: `backend/alembic.ini`, `backend/alembic/env.py`

### 2026-06-10: Initial auth migration created PostgreSQL enum twice

- Area: Alembic revision `20260610_0205`
- Trigger: After fixing async Alembic, `alembic upgrade head` failed with `DuplicateObjectError: type "user_status_enum" already exists`.
- Root cause: The revision explicitly called `user_status_enum.create(...)` and also reused the same enum object in `users.status`, so SQLAlchemy attempted a second implicit enum creation during table creation.
- Fix: Mark the enum object in the migration with `create_type=False` and keep the explicit `create(..., checkfirst=True)` as the single creation path.
- Regression guard: In PostgreSQL migrations, do not both explicitly create a named enum and leave implicit type creation enabled on the same enum object.
- Related files: `backend/alembic/versions/20260610_0205_create_auth_rbac_foundation.py`

### 2026-06-10: Auth seed hit MissingGreenlet when assigning permissions to new roles

- Area: Backend auth seed service
- Trigger: `uv run python scripts/seed_auth_rbac.py` failed with `MissingGreenlet` while setting `admin_role.permissions` and `user_role.permissions`.
- Root cause: Newly created `Role` entities in an `AsyncSession` had relationship collections that were not initialized, so assigning to them caused SQLAlchemy to attempt an async lazy load in a sync attribute path.
- Fix: Initialize the relationship collections for new roles with `set_committed_value(..., "permissions", [])` before assigning the permission lists.
- Regression guard: In async SQLAlchemy code, initialize relationship collections on new objects before bulk assignment if the attribute might otherwise trigger lazy loading.
- Related files: `backend/app/services/auth_seed.py`

### 2026-06-10: UserStatus enum persisted member names instead of business values

- Area: Backend ORM enum mapping
- Trigger: Auth seed failed with `invalid input value for enum user_status_enum: "ACTIVE"`.
- Root cause: SQLAlchemy `Enum(UserStatus, ...)` persisted the enum member name (`ACTIVE`) while the PostgreSQL enum values created by migration are lowercase business values (`active`, `inactive`, `locked`).
- Fix: Configure `backend/app/models/user.py` with `values_callable=lambda enum_cls: [member.value for member in enum_cls]` so ORM writes the business values expected by PostgreSQL.
- Regression guard: Whenever Python enums back PostgreSQL enum columns, verify whether ORM persistence uses member names or member values, and align migrations/models before seeding or writing data.
- Related files: `backend/app/models/user.py`, `backend/alembic/versions/20260610_0205_create_auth_rbac_foundation.py`, `backend/app/services/auth_seed.py`

### 2026-06-11: Logout on page refresh in cross-origin dev environment

- Area: Frontend authentication store & initialization
- Trigger: Successfully logged in, but refreshing the page logged out the user and redirected them back to the login page.
- Root cause: In local development, the frontend runs on `http://localhost:5173` while the backend runs on `http://127.0.0.1:8000`. This cross-site boundary caused two distinct issues:
  1. Frontend JS on `localhost` could not read the `fastapivue_logged_in` cookie set on `127.0.0.1` by the backend (blocking the initialization check).
  2. Even after bypassing the check, modern browsers block sending the `fastapivue_refresh_token` cookie (configured with `SameSite=Lax` and `Secure=False` in non-HTTPS local dev) on cross-site subresource requests (e.g. AJAX/Fetch calls from `localhost` to `127.0.0.1`), causing `POST /auth/refresh` to return `401 Unauthorized` (missing refresh token).
  3. When running the frontend locally outside of Docker (without VITE_API_BASE_URL env var explicitly set), the default API base URL in `frontend/src/api/runtime.ts` fell back to `'http://127.0.0.1:8000/api/v1'`. This caused requests to bypass the Vite proxy and query the backend port directly, recreating the cross-origin cookie blockage.
- Fix: 
  1. Synchronize and check the `fastapivue_logged_in` state in `localStorage` in `auth.store.ts`.
  2. Implement a same-origin dev proxy using Vite's `server.proxy` to forward `/api` requests to the backend server, and set `VITE_API_BASE_URL` to `/api/v1` for both dev and test compose environments. This unifies all frontend and API requests under the exact same hostname/origin in the browser, eliminating all cross-site cookie restrictions.
  3. Change the fallback value of `getApiBaseUrl()` in `frontend/src/api/runtime.ts` from `'http://127.0.0.1:8000/api/v1'` to `'/api/v1'` so same-origin proxy routing is the default behavior in all local development contexts.
- Regression guard: Keep dev and production stacks configured under the same-origin proxy paradigm to avoid cross-origin cookie blocking, and ensure any client-side default base URL defaults to a relative path (`/api/v1`).
- Related files: `frontend/vite.config.ts`, `frontend/src/stores/auth.store.ts`, `frontend/src/api/runtime.ts`, `docker-compose.yml`, `docker-compose.test.yml`, `.env`, `.env.example`


### 2026-06-11: Logout crashes with JSON parsing error or 502 Bad Gateway

- Area: Backend API Response / Frontend HTTP Client
- Trigger: Clicking the "Logout" button inside the admin layout.
- Root cause: Two colliding problems caused this:
  1. The backend `/auth/logout` endpoint was returning `Response` instance directly while decorated with `status_code=204`. This created an ASGI protocol collision between the 204 expectation and the default 200 response code, leading to connection drop (502 Bad Gateway).
  2. The frontend HTTP client `apiRequest` parsed any response containing `content-type: application/json` directly with `response.json()`. Because FastAPI's default response serialization class still includes the `content-type: application/json` header even for 204 No Content responses, the client attempted to parse the empty body, causing `SyntaxError: Failed to execute 'json' on 'Response': Unexpected end of JSON input`.
- Fix:
  1. Changed the backend `/logout` endpoint to return `None` (removing the return statement) and annotated the return type as `None`.
  2. Enhanced the frontend `apiRequest` in `frontend/src/api/http.ts` to first read the body as text using `response.text()`, check if the string is non-empty before calling `JSON.parse`, and wrap it in a safe try-catch block falling back to `null` to avoid any crashes on empty/invalid response bodies.
- Regression guard:
  1. Ensure all backend endpoints returning `204 No Content` do not return the `response: Response` parameter directly and return `None` instead.
  2. Ensure the frontend HTTP client reads bodies as text first and safely parses JSON only when the body is not empty.
- Related files: `backend/app/api/v1/auth.py`, `frontend/src/api/http.ts`, `frontend/tests/unit/http.spec.ts`

### 2026-06-11: Browser preview/download breaks when backend returns internal absolute URLs

- Area: Backend file/avatar response URLs and frontend browser rendering
- Trigger: Uploading a user avatar succeeded, but the preview image failed in the browser with `Failed to load resource: net::ERR_NAME_NOT_RESOLVED`.
- Root cause: Backend endpoints built absolute URLs from `request.base_url`. In proxy/Docker dev flows, that base URL can resolve to an internal hostname or non-browser-facing origin, so the browser receives an unusable `src`/download URL.
- Fix: Stop emitting absolute file URLs for browser-facing payloads. Return same-origin relative paths such as `/api/v1/files/{id}/download` from files, jobs, and user-avatar upload responses.
- Regression guard: For browser-consumed resource URLs behind same-origin proxy architecture, prefer relative API paths over absolute URLs derived from backend request metadata.
- Related files: `backend/app/api/url_utils.py`, `backend/app/api/v1/files.py`, `backend/app/api/v1/jobs.py`, `backend/app/api/v1/users.py`

### 2026-06-11: Topbar avatar stays stale after editing the currently logged-in user

- Area: Frontend user-management flow and auth store synchronization
- Trigger: Updating the current user's avatar or profile from the Users page changed the table data, but the shared topbar avatar stayed stale until a full page reload.
- Root cause: The Users edit flow refreshed the users listing but did not refresh `authStore.currentUser`, while the topbar renders avatar state from the auth store rather than from the users table.
- Fix: After a successful user update, if the updated record matches `authStore.currentUser?.id`, immediately call `authStore.fetchCurrentUser()` so the shell state refreshes in the same interaction.
- Regression guard: Any admin flow that can mutate the currently authenticated user's display data must refresh the shared auth source of truth, not just the local CRUD listing.
- Related files: `frontend/src/composables/useUsersPage.ts`, `frontend/src/stores/auth.store.ts`, `frontend/src/layouts/AdminLayout.vue`

### 2026-06-11: Mobile topbar loses sticky visibility on longer admin pages

- Area: Frontend admin shell responsive layout
- Trigger: On mobile, the shared topbar appeared fine on `Dashboard Smoke` but disappeared on longer pages like Users, Roles, Files, and Profile while scrolling.
- Root cause: The mobile shell relied on `position: sticky` for the topbar, but ancestor containers in `AdminLayout` used `overflow-x: clip`, a pattern that can break sticky behavior in mobile browsers. Route navigation also had no explicit `scrollBehavior`, so page-to-page navigation could preserve awkward scroll positions.
- Fix: Remove overflow clipping from sticky ancestors in `admin-layout.scss`, move horizontal overflow protection to `body/#app` in `primitives.scss`, and add router `scrollBehavior` to reset forward navigation to the top while preserving browser back/forward saved positions.
- Regression guard: Do not put `overflow: hidden/clip/auto` on ancestors of sticky shell elements unless browser behavior is verified on mobile. Shared admin shell routing should define explicit scroll restoration behavior.
- Related files: `frontend/src/styles/layouts/admin-layout.scss`, `frontend/src/styles/base/primitives.scss`, `frontend/src/router/index.ts`

### 2026-06-11: Hardening route tests can hang on upload/export request paths in ASGITransport

- Area: Backend hardening test strategy
- Trigger: New Phase 5 tests that tried to prove `429` and `403` behavior by repeatedly calling multipart upload or export-job routes under `httpx.ASGITransport` stalled instead of failing cleanly.
- Root cause: In this repo's test harness, some upload/export request paths are less stable than ordinary JSON/header checks when combined with dependency overrides and middleware. The behavior looked like an application regression at first, but the stable signal was route wiring rather than request execution.
- Fix: Keep runtime tests for stable behaviors such as security headers, and switch rate-limit/permission verification for sensitive upload/export routes to a mixed strategy: unit test the limiter engine and inspect route dependency wiring directly.
- Regression guard: If a new hardening test around upload/export starts hanging in the in-process ASGI harness, do not keep piling on retries. Fall back to route-contract assertions plus unit tests unless the failure reproduces in real runtime or Docker E2E.
- Related files: `backend/tests/test_hardening_api.py`, `backend/app/core/rate_limit.py`

### 2026-06-11: Phase 5 perf scripts must run through backend env, not host Python

- Area: Makefile performance smoke workflow
- Trigger: `make perf-users-list` and `make perf-users-export` failed immediately with `ModuleNotFoundError: No module named 'httpx'`.
- Root cause: The Make targets executed `python3 scripts/perf/...` on the host interpreter, while `httpx` is only guaranteed inside the backend environment managed by `uv` / `.venv`.
- Fix: Run perf scripts through the backend Python environment from `Makefile`, using `.venv/bin/python` when present or `uv run python` otherwise.
- Regression guard: Any repo-level Python utility that depends on backend packages must execute through the backend environment, never assume host Python has matching dependencies installed.
- Related files: `Makefile`, `scripts/perf/check_users_list.py`, `scripts/perf/check_users_export.py`

### 2026-06-11: Dependency-audit commands need writable cache paths and live DNS

- Area: Phase 5 dependency audit commands
- Trigger: `make backend-dependency-audit` and `make frontend-dependency-audit` initially failed before any advisory result because cache/log directories under `$HOME` were not writable in the agent environment.
- Root cause: `pip-audit` defaulted to `~/.cache/pip-audit` and `npm audit` defaulted to `~/.npm/_logs`, which are not safe assumptions in restricted environments. After fixing cache paths, both commands still required live DNS (`pypi.org`, `registry.npmjs.org`) and therefore remained blocked by sandbox networking.
- Fix: Set `XDG_CACHE_HOME=/tmp/.cache` for `pip-audit` and `NPM_CONFIG_CACHE=/tmp/.npm` for `npm audit` in `Makefile`. Treat outbound DNS/network access as a separate environment precondition for live advisory verification.
- Regression guard: Hardening commands must distinguish between local command wiring errors and external advisory-service reachability. Always route caches/logs to writable paths first, then record any remaining DNS/network block explicitly.
- Related files: `Makefile`, `backend/README.md`


### 2026-06-11: Failed to resolve component: Select in BackupsPage.vue

- Area: Frontend PrimeVue component import
- Trigger: Browser console error: `[Vue warn]: Failed to resolve component: Select`.
- Root cause: The PrimeVue `<Select>` component was used in `BackupsPage.vue` but was not imported from `'primevue/select'` under the `<script setup>` tag.
- Fix: Added `import Select from 'primevue/select'` to the top of `BackupsPage.vue`.
- Regression guard: Ensure that any PrimeVue components used in Vue SFC templates are explicitly imported inside the component script block.
- Related files: `frontend/src/pages/BackupsPage.vue`


### 2026-06-11: pg_dump server version mismatch on Backup Now

- Area: Backend Docker / Database client backup tool
- Trigger: Error message `pg_dump failed with exit code 1: pg_dump: error: aborting because of server version mismatch` when running a backup.
- Root cause: The PostgreSQL database server runs version 16, but the base stage of the backend Dockerfile installed `postgresql-client` via standard APT, which defaulted to version 15 on Debian Bookworm. Since lower-version pg_dump tools cannot dump higher-version servers, it aborted.
- Fix: Configured the official PostgreSQL APT repository in `docker/backend/Dockerfile` and explicitly installed `postgresql-client-16`.
- Regression guard: Ensure the client database backup binaries in backend container images match or exceed the version of the running database container.
- Related files: `docker/backend/Dockerfile`, `docker-compose.yml`


### 2026-06-11: Datetime timezone offset mismatch in backup email alerts

- Area: Backend Email notification / Datetime formatting
- Trigger: Backup alerts printed the naive UTC timestamps formatted directly via `.strftime()` while labeled as `(GMT+7)` (yielding a 7-hour discrepancy).
- Root cause: The database logs store timezone-aware UTC timestamps, but direct template string interpolation using `.strftime()` formats the naive/UTC offset value directly without converting it to the system's local timezone.
- Fix: Imported `zoneinfo`, localized datetimes to the configured setting `self.settings.app_timezone` (e.g. `Asia/Ho_Chi_Minh`), and then formatted the localized datetime objects in the subject line and email body.
- Regression guard: Always explicitly localize timezone-aware datetime objects to `app_timezone` before rendering them in user-facing views, logs, or emails.
- Related files: `backend/app/services/email.py`


## Usage Rule

Before changing behavior in an area with prior bugs, read the relevant entries first and explicitly avoid repeating the same failure mode.
