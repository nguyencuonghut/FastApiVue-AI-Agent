from __future__ import annotations

from collections.abc import Generator
from typing import Any
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.api.v1.auth import get_audit_log_service, get_auth_service
from app.db.session import get_db_session
from app.models import User, UserStatus


class MockSession:
    async def commit(self) -> None:
        pass


class MockAuthService:
    def __init__(self) -> None:
        self.session = MockSession()

    async def revoke_refresh_token(self, refresh_token: str) -> User | None:
        return User(id=uuid4(), email="test@example.com", status=UserStatus.ACTIVE)


class MockAuditLogService:
    async def log_event(self, **kwargs: Any) -> None:
        pass


@pytest.fixture
def override_logout_dependencies(app: FastAPI) -> Generator[None, None, None]:
    auth_service = MockAuthService()
    audit_service = MockAuditLogService()

    app.dependency_overrides[get_auth_service] = lambda: auth_service
    app.dependency_overrides[get_audit_log_service] = lambda: audit_service
    app.dependency_overrides[get_db_session] = lambda: MockSession()

    yield

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_logout_endpoint_response_status(
    app: FastAPI, client: AsyncClient, override_logout_dependencies: None
) -> None:
    # Set the refresh token cookie
    client.cookies.set("fastapivue_refresh_token", "dummy_token")

    response = await client.post("/api/v1/auth/logout")

    assert response.status_code == 204
    assert response.text == ""
    set_cookie = response.headers.get("set-cookie", "")

    assert "fastapivue_refresh_token" in set_cookie
    assert "max-age=0" in set_cookie.lower() or "expires=" in set_cookie.lower()
