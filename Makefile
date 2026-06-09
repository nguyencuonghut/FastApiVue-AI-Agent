SHELL := /bin/bash

UV_CACHE_DIR ?= /tmp/uv-cache
DOCKER_TEST_COMPOSE := docker compose -f docker-compose.test.yml

.PHONY: \
	backend-lint \
	backend-format-check \
	backend-typecheck \
	backend-test \
	backend-security \
	backend-check \
	frontend-lint \
	frontend-format-check \
	frontend-typecheck \
	frontend-test-unit \
	frontend-test-e2e \
	frontend-check \
	frontend-check-e2e \
	check \
	docker-test-backend \
	docker-test-frontend \
	docker-test-e2e \
	docker-test

backend-lint:
	cd backend && if [ -x .venv/bin/ruff ]; then .venv/bin/ruff check .; else UV_CACHE_DIR=$(UV_CACHE_DIR) uv run ruff check .; fi

backend-format-check:
	cd backend && if [ -x .venv/bin/ruff ]; then .venv/bin/ruff format --check .; else UV_CACHE_DIR=$(UV_CACHE_DIR) uv run ruff format --check .; fi

backend-typecheck:
	cd backend && if [ -x .venv/bin/mypy ]; then .venv/bin/mypy .; else UV_CACHE_DIR=$(UV_CACHE_DIR) uv run mypy .; fi

backend-test:
	cd backend && if [ -x .venv/bin/pytest ]; then .venv/bin/pytest tests --cov=app --cov-report=term-missing; else UV_CACHE_DIR=$(UV_CACHE_DIR) uv run pytest tests --cov=app --cov-report=term-missing; fi

backend-security:
	cd backend && if [ -x .venv/bin/bandit ]; then .venv/bin/bandit -c pyproject.toml -r app; else UV_CACHE_DIR=$(UV_CACHE_DIR) uv run bandit -c pyproject.toml -r app; fi

backend-check: backend-lint backend-format-check backend-typecheck backend-test backend-security

frontend-lint:
	npm --prefix frontend run lint

frontend-format-check:
	npm --prefix frontend run format:check

frontend-typecheck:
	npm --prefix frontend run typecheck

frontend-test-unit:
	npm --prefix frontend run test:unit

frontend-test-e2e:
	npm --prefix frontend run test:e2e

frontend-check: frontend-lint frontend-format-check frontend-typecheck frontend-test-unit

frontend-check-e2e: frontend-check frontend-test-e2e

check: backend-check frontend-check

docker-test-backend:
	$(DOCKER_TEST_COMPOSE) run --rm backend-test

docker-test-frontend:
	$(DOCKER_TEST_COMPOSE) run --rm frontend-test

docker-test-e2e:
	$(DOCKER_TEST_COMPOSE) run --rm e2e-test

docker-test: docker-test-backend docker-test-frontend docker-test-e2e
