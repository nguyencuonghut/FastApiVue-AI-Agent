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
7. `src/styles/tokens.css` is the source of truth for dark/light theme tokens

Vue SFCs must not use `scoped style`. Keep styles in adjacent CSS files and rely on explicit class namespaces per component/layout/page.

The frontend lint pipeline should fail if any `.vue` file contains `<style scoped>`.

Vitest unit tests must not scan Playwright specs. Keep `tests/unit` and `tests/e2e` separated and constrain Vitest `include` patterns explicitly.

PrimeVue is configured with a custom preset and `darkModeSelector` bound to `.app-dark` so manual theme switching stays consistent across shared components.
