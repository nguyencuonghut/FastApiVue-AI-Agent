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

## Usage Rule

Before changing behavior in an area with prior bugs, read the relevant entries first and explicitly avoid repeating the same failure mode.
