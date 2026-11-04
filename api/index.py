"""Vercel Python ASGI entrypoint for the Elas Conectadas MCP API."""
from elas_conectadas_mcp.http_app import app

__all__ = ["app"]
