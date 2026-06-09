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

## Usage Rule

Before changing behavior in an area with prior bugs, read the relevant entries first and explicitly avoid repeating the same failure mode.
