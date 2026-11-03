import httpx
import pytest

from elas_conectadas_mcp.connectors.ibge import IBGEConnector


@pytest.mark.asyncio
async def test_list_states_uses_ibge_api():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/estados")
        return httpx.Response(
            200,
            json=[{"id": 35, "sigla": "SP", "nome": "São Paulo", "regiao": {"nome": "Sudeste"}}],
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await IBGEConnector(client).list_states()

    assert result == [{"id": 35, "sigla": "SP", "nome": "São Paulo", "regiao": "Sudeste"}]


@pytest.mark.asyncio
async def test_list_municipalities_validates_uf_before_request():
    connector = IBGEConnector()
    with pytest.raises(ValueError):
        await connector.list_municipalities("São Paulo")


@pytest.mark.asyncio
async def test_get_municipality_returns_territorial_data():
    payload = {
        "id": 3550308,
        "nome": "São Paulo",
        "microrregiao": {
            "mesorregiao": {
                "UF": {
                    "sigla": "SP",
                    "nome": "São Paulo",
                    "regiao": {"nome": "Sudeste"},
                }
            }
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await IBGEConnector(client).get_municipality(3550308)

    assert result["nome"] == "São Paulo"
    assert result["uf"] == "SP"
    assert result["regiao"] == "Sudeste"
