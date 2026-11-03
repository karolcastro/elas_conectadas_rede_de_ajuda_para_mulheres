import pytest

from elas_conectadas_mcp.services.health_search import HealthSearchService

class FakeIBGE:
    async def list_municipalities(self, uf):
        assert uf == "SP"
        return [{"id": 3550308, "nome": "São Paulo"}, {"id": 3509502, "nome": "Campinas"}]

class FakeDEMAS:
    async def search_establishments(self, **kwargs):
        self.kwargs = kwargs
        return {"record_count": 1, "records": [{"codigo_cnes": "1234567"}]}

@pytest.mark.asyncio
async def test_resolves_ibge_code_and_searches_cnes_with_six_digit_municipality():
    demas = FakeDEMAS()
    service = HealthSearchService(ibge=FakeIBGE(), demas=demas)
    result = await service.search_by_municipality("Sao Paulo", "sp")
    assert result["municipality"] == "São Paulo"
    assert result["ibge_municipality_code"] == 3550308
    assert result["cnes_municipality_code"] == 355030
    assert demas.kwargs["municipality_code"] == 355030
    assert demas.kwargs["status"] == 1
    assert result["results"]["record_count"] == 1

@pytest.mark.asyncio
async def test_rejects_unknown_municipality():
    service = HealthSearchService(ibge=FakeIBGE(), demas=FakeDEMAS())
    with pytest.raises(ValueError, match="não encontrado"):
        await service.search_by_municipality("Santos", "SP")

@pytest.mark.asyncio
async def test_rejects_blank_municipality():
    service = HealthSearchService(ibge=FakeIBGE(), demas=FakeDEMAS())
    with pytest.raises(ValueError, match="Informe o nome"):
        await service.search_by_municipality(" ", "SP")
