"""HTTP ASGI adapter for local testing and future hosting.

The MCP stdio entrypoint remains available and unchanged.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse

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


# FastMCP 1.x uses server settings for Streamable HTTP configuration.
# The stdio transport remains the default when main() calls mcp.run().
mcp.settings.stateless_http = True
app = mcp.streamable_http_app()
