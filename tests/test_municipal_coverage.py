from __future__ import annotations

from typing import Any

import pytest

from elas_conectadas_mcp.services.municipal_coverage import MunicipalCoverageService


class FakeIBGE:
    async def list_states(self) -> list[dict[str, Any]]:
        return [
            {"sigla": "AA", "nome": "Estado A", "regiao": "Norte"},
            {"sigla": "BB", "nome": "Estado B", "regiao": "Sul"},
        ]

    async def list_municipalities(self, uf: str) -> list[dict[str, Any]]:
        return {
            "AA": [{"id": 1, "nome": "Alfa"}, {"id": 2, "nome": "Beta"}],
            "BB": [{"id": 3, "nome": "Gama"}],
        }[uf]


class FakeRegistry:
    def list_services(self, *, include_stale: bool) -> dict[str, Any]:
        assert include_stale is True
        return {
            "as_of": "2026-11-10",
            "count": 4,
            "services": [
                {
                    "id": "local-alfa", "state": "AA", "municipality": "Alfa",
                    "catalog_status": "verified",
                },
                {"id": "statewide-aa", "coverage": "AA", "catalog_status": "verified"},
                {
                    "id": "local-beta-expired", "state": "AA", "municipality": "Beta",
                    "catalog_status": "expired",
                },
                {
                    "id": "local-gama", "state": "BB", "municipality": "Gama",
                    "catalog_status": "verified",
                },
            ],
        }


@pytest.mark.asyncio
async def test_audit_counts_only_verified_local_records_as_municipal_coverage():
    service = MunicipalCoverageService(ibge=FakeIBGE(), protection_registry=FakeRegistry())

    result = await service.audit()

    assert result["total_municipios_ibge"] == 3
    assert result["municipios_com_registro_local_valido"] == 2
    assert result["municipios_sem_registro_local_valido"] == 1
    assert result["cobertura_local_percentual"] == 66.67
    assert result["municipios_sem_registro_amostra"] == [
        {"municipio": "Beta", "uf": "AA", "codigo_ibge": 2}
    ]
    assert result["registros_estaduais_ou_nacionais_validos"] == 2
    assert "não comprovam unidade física" in result["nota_metodologica"]


@pytest.mark.asyncio
async def test_audit_can_filter_by_state():
    service = MunicipalCoverageService(ibge=FakeIBGE(), protection_registry=FakeRegistry())

    result = await service.audit(uf="bb")

    assert result["uf_filtro"] == "BB"
    assert result["total_municipios_ibge"] == 1
    assert result["municipios_com_registro_local_valido"] == 1


@pytest.mark.asyncio
async def test_audit_rejects_invalid_state_and_sample_limit():
    service = MunicipalCoverageService(ibge=FakeIBGE(), protection_registry=FakeRegistry())

    with pytest.raises(ValueError, match="sigla"):
        await service.audit(uf="Estado A")
    with pytest.raises(ValueError, match="limite"):
        await service.audit(missing_limit=501)


@pytest.mark.asyncio
async def test_research_queue_includes_uncovered_and_expired_local_records():
    service = MunicipalCoverageService(ibge=FakeIBGE(), protection_registry=FakeRegistry())

    result = await service.research_queue()

    assert result["total_municipios_na_fila"] == 1
    assert result["fila"][0]["municipio"] == "Beta"
    assert result["fila"][0]["status_pesquisa"] == "aguardando_pesquisa"
    assert result["fila"][0]["registros_locais_pendentes_revisao"] == 1
    assert result["proxima_pagina_offset"] is None
    assert "não ausência de serviços" in result["nota_metodologica"]


@pytest.mark.asyncio
async def test_research_queue_supports_state_filter_and_pagination():
    service = MunicipalCoverageService(ibge=FakeIBGE(), protection_registry=FakeRegistry())

    result = await service.research_queue(uf="aa", limit=1, offset=0)

    assert result["uf_filtro"] == "AA"
    assert result["total_municipios_na_fila"] == 1
    assert len(result["fila"]) == 1


@pytest.mark.asyncio
async def test_research_queue_rejects_invalid_pagination():
    service = MunicipalCoverageService(ibge=FakeIBGE(), protection_registry=FakeRegistry())

    with pytest.raises(ValueError, match="limite"):
        await service.research_queue(limit=0)
    with pytest.raises(ValueError, match="deslocamento"):
        await service.research_queue(offset=-1)
