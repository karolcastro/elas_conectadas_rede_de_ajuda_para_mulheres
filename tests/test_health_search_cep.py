import pytest

from elas_conectadas_mcp.services.health_search import HealthSearchService


class FakeIBGE:
    async def list_municipalities(self, uf):
        assert uf == "SP"
        return [{"id": 3550308, "nome": "São Paulo"}]

class FakeDEMAS:
    async def search_establishments(self, **kwargs):
        return {"record_count": 1, "records": [{"codigo_cnes": "123"}]}

class FakeViaCEP:
    async def lookup(self, cep):
        assert cep == "01001000"
        return {"cep": "01001-000", "municipality": "São Paulo", "uf": "SP", "ibge_municipality_code": 3550308}

@pytest.mark.asyncio
async def test_search_by_cep_resolves_municipality_and_returns_cnes_results():
    service = HealthSearchService(ibge=FakeIBGE(), demas=FakeDEMAS(), viacep=FakeViaCEP())
    result = await service.search_by_cep("01001000")
    assert result["location"]["municipality"] == "São Paulo"
    assert result["municipal_health_facilities"]["municipality"] == "São Paulo"
    assert result["municipal_health_facilities"]["results"]["record_count"] == 1
