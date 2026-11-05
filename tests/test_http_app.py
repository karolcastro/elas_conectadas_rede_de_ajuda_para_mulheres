"""Tests for the local Streamable HTTP adapter."""

import httpx
import pytest

from elas_conectadas_mcp.http_app import app


@pytest.mark.asyncio
async def test_health_endpoint_returns_minimal_liveness_payload() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://localhost:8000",
        headers={"host": "localhost:8000"},
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Elas Conectadas MCP",
        "transport": "streamable-http",
    }
