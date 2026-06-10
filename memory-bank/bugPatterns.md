# Bug Patterns

## Current Status

No historical application bugs are recorded yet in this workspace snapshot.

That means agents must not assume there were no bugs. It means bug memory has not been populated yet.

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

## Usage Rule

Before changing behavior in an area with prior bugs, read the relevant entries first and explicitly avoid repeating the same failure mode.
