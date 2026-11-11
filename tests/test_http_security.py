import httpx
import pytest

from elas_conectadas_mcp.connectors.http_security import (
    UnsafeUpstreamResponse,
    get_json,
)


@pytest.mark.asyncio
async def test_get_json_disables_redirects():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.extensions.get("timeout") is not None
        return httpx.Response(302, headers={"location": "https://attacker.example/payload"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(UnsafeUpstreamResponse, match="Redirecionamento"):
            await get_json(
                client=client,
                url="https://trusted.example/api",
                timeout=httpx.Timeout(2.0),
            )


@pytest.mark.asyncio
async def test_get_json_rejects_response_larger_than_limit():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"x" * 33)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(UnsafeUpstreamResponse, match="excede"):
            await get_json(
                client=client,
                url="https://trusted.example/api",
                timeout=httpx.Timeout(2.0),
                max_bytes=32,
            )


@pytest.mark.asyncio
async def test_get_json_rejects_non_json_content_type():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"<html>not json</html>",
            headers={"content-type": "text/html"},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(UnsafeUpstreamResponse, match="não retornou conteúdo JSON"):
            await get_json(
                client=client,
                url="https://trusted.example/api",
                timeout=httpx.Timeout(2.0),
            )


@pytest.mark.asyncio
async def test_get_json_rejects_non_https_destination():
    with pytest.raises(UnsafeUpstreamResponse, match="HTTPS obrigatório"):
        await get_json(
            client=None,
            url="http://trusted.example/api",
            timeout=httpx.Timeout(2.0),
        )


@pytest.mark.asyncio
async def test_get_json_accepts_bounded_json_response():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await get_json(
            client=client,
            url="https://trusted.example/api",
            timeout=httpx.Timeout(2.0),
        )

    assert result == {"ok": True}
