"""ASGI entrypoint for the Vercel-hosted Streamable HTTP MCP service.

The original stdio entrypoint remains available for local MCP clients.
"""

from __future__ import annotations

import os

from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

from elas_conectadas_mcp.server import mcp


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Public liveness check; returns no user or service-directory data."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "Elas Conectadas MCP",
            "transport": "streamable-http",
        }
    )


def _allowed_hosts() -> list[str]:
    """Allow only hostnames assigned to this Vercel deployment/project."""
    hosts = {
        "elas-conectadas-rede-de-ajuda-para-mulheres-karolinycosta-3770.vercel.app",
    }
    for variable in (
        "VERCEL_URL",
        "VERCEL_BRANCH_URL",
        "VERCEL_PROJECT_PRODUCTION_URL",
    ):
        value = os.getenv(variable, "").strip().lower()
        if value:
            hosts.add(value.removeprefix("https://").removeprefix("http://").rstrip("/"))
    return sorted(host for host in hosts if host)


security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        value
        for host in _allowed_hosts()
        for value in (host, f"{host}:443")
    ],
)

# Stateless HTTP avoids relying on in-memory MCP sessions across serverless invocations.
# The existing stdio transport remains unchanged for local MCP clients.
app = mcp.streamable_http_app(
    transport_security=security,
    stateless_http=True,
    max_request_body_size=1 * 1024 * 1024,
)
