"""HTTP ASGI adapter for local testing and future hosting.

The MCP stdio entrypoint remains available and unchanged.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from mcp.server.transport_security import TransportSecuritySettings

from elas_conectadas_mcp.server import mcp


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Return a minimal liveness response without personal or directory data."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "Elas Conectadas MCP",
            "transport": "streamable-http",
        }
    )


_local_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        "localhost",
        "localhost:8000",
        "127.0.0.1",
        "127.0.0.1:8000",
        "testserver",
    ],
)

app = mcp.streamable_http_app(
    transport_security=_local_security,
    stateless_http=True,
    max_request_body_size=1 * 1024 * 1024,
)
