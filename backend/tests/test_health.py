import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_health_returns_expected_payload(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "X-Request-ID" in response.headers


@pytest.mark.asyncio
async def test_api_v1_health_returns_expected_payload(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
