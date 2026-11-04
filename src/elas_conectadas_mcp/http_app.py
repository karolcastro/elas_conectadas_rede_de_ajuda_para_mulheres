"""ASGI entrypoint for the authenticated Streamable HTTP MCP transport."""
from __future__ import annotations

import hmac
import os
from collections.abc import Awaitable, Callable
from typing import Any

from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

from elas_conectadas_mcp.server import mcp


class BearerTokenMiddleware:
    """Require a deployment-provided bearer token for every MCP request."""

    def __init__(self, app: Callable[..., Awaitable[None]], token: str | None) -> None:
        self.app = app
        self.token = token

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if not self.token:
            response = JSONResponse(
                {"error": "MCP endpoint is not configured with an access token."},
                status_code=503,
            )
            await response(scope, receive, send)
            return

        headers = {key.lower(): value for key, value in scope.get("headers", [])}
        authorization = headers.get(b"authorization", b"").decode("latin-1")
        scheme, _, supplied = authorization.partition(" ")
        if scheme.lower() != "bearer" or not hmac.compare_digest(supplied, self.token):
            response = JSONResponse(
                {"error": "A valid bearer token is required."},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)


def _required_csv_env(name: str) -> list[str]:
    values = [item.strip() for item in os.getenv(name, "").split(",") if item.strip()]
    if not values:
        raise RuntimeError(
            f"{name} must contain explicit comma-separated host/origin allowlist values."
        )
    return values


transport_security = TransportSecuritySettings(
    allowed_hosts=_required_csv_env("ELAS_MCP_ALLOWED_HOSTS"),
    allowed_origins=_required_csv_env("ELAS_MCP_ALLOWED_ORIGINS"),
)

# Stateless JSON responses avoid relying on in-memory sessions across serverless invocations.
mcp_asgi_app = mcp.streamable_http_app(
    streamable_http_path="/api/mcp",
    stateless_http=True,
    json_response=True,
    transport_security=transport_security,
)

app = BearerTokenMiddleware(mcp_asgi_app, token=os.getenv("ELAS_MCP_BEARER_TOKEN"))
