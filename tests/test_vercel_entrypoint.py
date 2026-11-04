"""Checks for the Vercel ASGI adapter without making network requests."""

from api.index import app, security


def test_vercel_adapter_exposes_mcp_and_health_routes() -> None:
    paths = {route.path for route in app.routes}
    assert "/mcp" in paths
    assert "/health" in paths


def test_vercel_adapter_keeps_dns_rebinding_protection_enabled() -> None:
    assert security.enable_dns_rebinding_protection is True
    assert any(
        host == "elas-conectadas-rede-de-ajuda-para-mulheres-karolinycosta-3770.vercel.app"
        for host in security.allowed_hosts
    )
