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

## Usage Rule

Before changing behavior in an area with prior bugs, read the relevant entries first and explicitly avoid repeating the same failure mode.
