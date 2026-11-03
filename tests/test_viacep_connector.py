import httpx
import pytest

from elas_conectadas_mcp.connectors.viacep import ViaCEPConnector


@pytest.mark.asyncio
async def test_lookup_returns_minimized_location_without_street_or_postal_code():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/01001000/json/")
        return httpx.Response(200, json={"cep":"01001-000","logradouro":"Praça da Sé","bairro":"Sé","localidade":"São Paulo","uf":"SP","ibge":"3550308"})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await ViaCEPConnector(client).lookup("01001-000")
    assert result["municipality"] == "São Paulo"
    assert result["ibge_municipality_code"] == 3550308
    assert "cep" not in result
    assert "logradouro" not in result
    assert "bairro" not in result
    assert "privacy_notice" in result

@pytest.mark.asyncio
async def test_invalid_cep_is_rejected_without_request():
    with pytest.raises(ValueError, match="oito dígitos"):
        await ViaCEPConnector().lookup("123")

@pytest.mark.asyncio
async def test_unknown_cep_is_reported():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"erro": True})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ValueError, match="não encontrado"):
            await ViaCEPConnector(client).lookup("99999999")
