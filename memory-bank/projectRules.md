# Project Rules

## Rule 1: Never Guess

If a fact is not verified from code, tests, command output, or cited documentation, the agent must say it is unverified and inspect first.

## Rule 2: Read Bug History First

Before touching an area that has known defects or regressions, read `memory-bank/bugPatterns.md`.

## Rule 3: Preserve Memory After Fixes

Every resolved bug should leave behind a durable record:

- trigger
- root cause
- fix
- regression test or guardrail

## Rule 4: Match Existing Coding Style

When code exists, follow its:

- naming conventions
- file placement
- framework idioms
- validation patterns
- test structure

Do not introduce a new style unless the user explicitly asks for it or the existing pattern is demonstrably broken.

## Rule 4A: No Style Block In Vue SFC

Do not use `<style>` blocks in `.vue` files.

Frontend styles must live in the centralized `src/styles/` tree, preferably as `.scss` files with explicit class naming. Style isolation should come from structure and naming, not from Vue style blocks.

## Rule 5: Use Verified Tech Stack Only

The source of truth is `memory-bank/techContext.md`.

If the codebase proves the file wrong or incomplete, update the file instead of silently assuming.

## Rule 6: Prefer Reuse Over New Structure

Search for extension points before creating files, folders, services, or abstractions.

## Rule 7: Record Durable Project Knowledge

Update the Memory Bank when a task reveals:

- a recurring bug pattern
- a stable architectural rule
- a tech stack fact
- a workflow constraint

## Rule 8: Evidence Beats Confidence

Technical claims should be backed by:

- file references
- command output
- tests
- linked upstream sources

## Rule 9: Keep Dark/Light Theme Consistent

Dark/light mode is a system-wide style contract.

Buttons, menus, headers, data tables, form inputs, dialogs, cards, tabs, and notifications must use shared theme tokens and remain visually consistent across all pages.

Do not hardcode colors in page/component code. Add or reuse semantic tokens/classes instead.

Any UI change that affects shared components must be checked in both dark and light mode before completion.

## Rule 10: Enterprise Performance And Security

The boilerplate must be designed at enterprise level.

Do not load tens of thousands of rows into a normal API response or frontend store. Use server-side pagination/filter/sort, cursor pagination for large datasets, and virtual scrolling only where appropriate.

Heavy import/export must use async jobs, chunk/stream processing, progress tracking, audit log, error report, and permissions.

Security-sensitive endpoints must include RBAC, validation, rate limit where appropriate, audit logging, and tests.

Secrets must never be committed. Database access must use ORM/query builder safely or parameterized queries. Production must enforce HTTPS, secure headers, CORS by environment, and dependency/container scanning.

Production deployment is not acceptable without observability, backup/restore runbooks, secret management, SLO/alerts, and passing compliance gates or approved waivers.
