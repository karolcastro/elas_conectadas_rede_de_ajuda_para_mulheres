import httpx
import pytest

from elas_conectadas_mcp.connectors.demas import DEMASConnector


@pytest.mark.asyncio
async def test_search_establishments_sends_documented_filters():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/cnes/estabelecimentos")
        assert request.url.params["codigo_municipio"] == "3550308"
        assert request.url.params["status"] == "1"
        assert request.url.params["limit"] == "20"
        return httpx.Response(200, json=[{"codigo_cnes": "123", "nome_fantasia": "Unidade teste"}])

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await DEMASConnector(client).search_establishments(
            municipality_code=3550308, status=1, limit=20
        )

    assert result["record_count"] == 1
    assert result["records"][0]["codigo_cnes"] == "123"
    assert "não confirma agenda" in result["important_notice"]


@pytest.mark.asyncio
async def test_get_establishment_by_cnes_code():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/cnes/estabelecimentos/1234567")
        return httpx.Response(200, json={"codigo_cnes": "1234567"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await DEMASConnector(client).get_establishment(1234567)

    assert result["records"] == [{"codigo_cnes": "1234567"}]


@pytest.mark.asyncio
async def test_list_ubs_uses_pagination():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/assistencia-a-saude/unidade-basicas-de-saude")
        assert request.url.params["limit"] == "50"
        assert request.url.params["offset"] == "100"
        return httpx.Response(200, json={"data": [{"cnes": "987"}]})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await DEMASConnector(client).list_basic_health_units(limit=50, offset=100)

    assert result["records"] == [{"cnes": "987"}]


@pytest.mark.asyncio
async def test_rejects_limit_above_documented_establishment_maximum():
    connector = DEMASConnector()
    with pytest.raises(ValueError):
        await connector.search_establishments(limit=21)


@pytest.mark.asyncio
async def test_rejects_invalid_status():
    connector = DEMASConnector()
    with pytest.raises(ValueError):
        await connector.search_establishments(status=2)
