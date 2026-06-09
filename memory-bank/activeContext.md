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

## Next Useful Steps

1. Implement Phase 1 Step 4 Docker dev according to `docs/phase-1-scaffold-implementation-plan.md`.
2. Populate bug history when the first real defects are fixed.
3. Keep `techContext.md` and `projectRules.md` synchronized with real project discoveries.
