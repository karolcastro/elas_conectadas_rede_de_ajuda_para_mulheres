"""ASGI entrypoint for Vercel-hosted Elas Conectadas MCP and chat."""
from __future__ import annotations
import os
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse
from elas_conectadas_mcp.server import mcp
from api.chat_ui import register_chat_routes

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({
        "status": "ok",
        "service": "Elas Conectadas",
        "transport": "streamable-http",
        "chat": "configured" if os.getenv("GEMINI_API_KEY") else "missing_api_key",
    })

register_chat_routes(mcp)

def _allowed_hosts() -> list[str]:
    hosts = {
        "elas-conectadas-rede-de-ajuda-para-mulheres-karolinycosta-3770.vercel.app",
        "elas-conectadas-rede-de-ajuda-para.vercel.app",
    }
    for variable in ("VERCEL_URL", "VERCEL_BRANCH_URL", "VERCEL_PROJECT_PRODUCTION_URL"):
        value = os.getenv(variable, "").strip().lower()
        if value:
            hosts.add(value.removeprefix("https://").removeprefix("http://").rstrip("/"))
    return sorted(host for host in hosts if host)

security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[value for host in _allowed_hosts() for value in (host, f"{host}:443")],
)

app = mcp.streamable_http_app(
    transport_security=security,
    stateless_http=True,
    max_request_body_size=1 * 1024 * 1024,
)
