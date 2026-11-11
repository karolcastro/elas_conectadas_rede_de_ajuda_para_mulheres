"""Auditoria de cobertura municipal usando a malha oficial de localidades do IBGE."""

from __future__ import annotations

from typing import Any


class MunicipalCoverageService:
    """Compara todos os municípios do IBGE com referências locais válidas do catálogo."""

    def __init__(self, *, ibge: Any, protection_registry: Any) -> None:
        self.ibge = ibge
        self.protection_registry = protection_registry

    async def audit(
        self,
        *,
        uf: str | None = None,
        missing_limit: int = 100,
    ) -> dict[str, Any]:
        """Retorna cobertura exata por município sem inferir atendimento local.

        Registros nacionais e estaduais são contabilizados separadamente e não
        transformam um município em município com serviço local cadastrado.
        """
        if uf is not None:
            normalized_uf = uf.strip().upper()
            if len(normalized_uf) != 2 or not normalized_uf.isalpha():
                raise ValueError("Informe uma sigla de UF válida com duas letras.")
        else:
            normalized_uf = None

        if isinstance(missing_limit, bool) or not isinstance(missing_limit, int):
            raise TypeError("O limite deve ser um número inteiro.")
        if missing_limit < 0 or missing_limit > 500:
            raise ValueError("O limite deve estar entre 0 e 500.")

        states = await self.ibge.list_states()
        if normalized_uf:
            states = [state for state in states if state["sigla"] == normalized_uf]
            if not states:
                raise ValueError("UF não encontrada na lista oficial do IBGE.")

        catalog = self.protection_registry.list_services(include_stale=True)
        records = catalog.get("services", [])
        valid_records = [
            item for item in records if item.get("catalog_status") == "verified"
        ]

        municipalities_by_state: dict[str, list[dict[str, Any]]] = {}
        for state in states:
            state_uf = state["sigla"]
            municipalities_by_state[state_uf] = await self.ibge.list_municipalities(state_uf)

        result_by_state = []
        missing_municipalities = []
        total_municipalities = 0
        covered_municipalities = 0

        for state in states:
            state_uf = state["sigla"]
            municipalities = municipalities_by_state[state_uf]
            total_municipalities += len(municipalities)
            state_records = [
                item for item in valid_records
                if item.get("state") == state_uf
                or state_uf in (item.get("ufs") or [])
                or item.get("coverage") == state_uf
            ]
            state_covered = 0
            state_missing = 0

            for municipality in municipalities:
                name = municipality["nome"]
                local_records = [
                    item for item in state_records
                    if (
                        str(item.get("municipality", "")).strip().casefold()
                        == name.strip().casefold()
                    )
                ]
                if local_records:
                    state_covered += 1
                    covered_municipalities += 1
                else:
                    state_missing += 1
                    if len(missing_municipalities) < missing_limit:
                        missing_municipalities.append({
                            "municipio": name,
                            "uf": state_uf,
                            "codigo_ibge": municipality.get("id"),
                        })

            result_by_state.append({
                "uf": state_uf,
                "estado": state["nome"],
                "regiao": state.get("regiao"),
                "total_municipios_ibge": len(municipalities),
                "municipios_com_registro_local_valido": state_covered,
                "municipios_sem_registro_local_valido": state_missing,
                "cobertura_local_percentual": round(
                    state_covered / len(municipalities) * 100, 2
                ) if municipalities else 0.0,
                "registros_estaduais_ou_nacionais_validos": len(state_records),
            })

        missing_total = total_municipalities - covered_municipalities
        return {
            "fonte_territorial": "IBGE — API de Localidades",
            "data_consulta": catalog.get("as_of"),
            "uf_filtro": normalized_uf,
            "total_municipios_ibge": total_municipalities,
            "municipios_com_registro_local_valido": covered_municipalities,
            "municipios_sem_registro_local_valido": missing_total,
            "cobertura_local_percentual": round(
                covered_municipalities / total_municipalities * 100, 2
            ) if total_municipalities else 0.0,
            "estados": result_by_state,
            "municipios_sem_registro_amostra": missing_municipalities,
            "limite_amostra": missing_limit,
            "total_registros_catalogo": catalog.get("count", len(records)),
            "registros_validos_considerados": len(valid_records),
            "registros_com_revisao_vencida_ou_pendente": sum(
                1 for item in records if item.get("catalog_status") != "verified"
            ),
            "nota_metodologica": (
                "Cobertura municipal significa apenas que existe ao menos um registro "
                "local com revisão válida no catálogo. Referências estaduais ou nacionais "
                "são contabilizadas separadamente e não comprovam unidade física no município. "
                "A auditoria não confirma funcionamento, agenda, gratuidade ou disponibilidade. "
                "Municípios sem registro local podem possuir serviços ainda não cadastrados."
            ),
        }

    async def research_queue(
        self,
        *,
        uf: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Monta fila paginada de pesquisa para municípios sem registro local válido."""
        if uf is not None:
            normalized_uf = uf.strip().upper()
            if len(normalized_uf) != 2 or not normalized_uf.isalpha():
                raise ValueError("Informe uma sigla de UF válida com duas letras.")
        else:
            normalized_uf = None
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError("O limite deve ser um número inteiro.")
        if isinstance(offset, bool) or not isinstance(offset, int):
            raise TypeError("O deslocamento deve ser um número inteiro.")
        if limit < 1 or limit > 500:
            raise ValueError("O limite deve estar entre 1 e 500.")
        if offset < 0 or offset > 100000:
            raise ValueError("O deslocamento deve estar entre 0 e 100000.")

        states = await self.ibge.list_states()
        if normalized_uf:
            states = [state for state in states if state["sigla"] == normalized_uf]
            if not states:
                raise ValueError("UF não encontrada na lista oficial do IBGE.")

        catalog = self.protection_registry.list_services(include_stale=True)
        records = catalog.get("services", [])
        verified = [item for item in records if item.get("catalog_status") == "verified"]
        queue = []
        state_summary = []

        for state in states:
            state_uf = state["sigla"]
            municipalities = await self.ibge.list_municipalities(state_uf)
            state_refs = [
                item for item in verified
                if not item.get("municipality")
                and (
                    item.get("state") == state_uf
                    or state_uf in (item.get("ufs") or [])
                    or item.get("coverage") in {state_uf, "Brasil"}
                )
            ]
            uncovered = 0
            for municipality in municipalities:
                name = municipality["nome"]
                matching = [
                    item for item in records
                    if str(item.get("municipality", "")).strip().casefold() == name.strip().casefold()
                    and (
                        item.get("state") == state_uf
                        or state_uf in (item.get("ufs") or [])
                        or item.get("coverage") == state_uf
                    )
                ]
                if any(item.get("catalog_status") == "verified" for item in matching):
                    continue
                uncovered += 1
                stale_local = [
                    item for item in matching
                    if item.get("catalog_status") != "verified"
                ]
                queue.append({
                    "municipio": name,
                    "uf": state_uf,
                    "codigo_ibge": municipality.get("id"),
                    "prioridade": "alta",
                    "status_pesquisa": "aguardando_pesquisa",
                    "registros_locais_pendentes_revisao": len(stale_local),
                    "referencias_estaduais_ou_nacionais": len(state_refs),
                    "proximas_acoes": [
                        "Pesquisar portal oficial da prefeitura e secretaria municipal "
                        "responsável.",
                        "Pesquisar órgãos estaduais e a rede oficial de atendimento.",
                        "Verificar existência, público atendido, endereço público e contato "
                        "institucional.",
                        "Confirmar gratuidade, funcionamento, critérios e data da fonte.",
                        "Cadastrar somente após validação documental; nunca publicar endereço "
                        "sigiloso de abrigo.",
                    ],
                })
            state_summary.append({
                "uf": state_uf,
                "estado": state["nome"],
                "total_municipios_ibge": len(municipalities),
                "municipios_na_fila": uncovered,
                "referencias_estaduais_ou_nacionais_validas": len(state_refs),
            })

        queue.sort(key=lambda item: (item["uf"], item["municipio"].casefold()))
        total = len(queue)
        return {
            "fonte_territorial": "IBGE — API de Localidades",
            "data_consulta_catalogo": catalog.get("as_of"),
            "uf_filtro": normalized_uf,
            "total_municipios_na_fila": total,
            "offset": offset,
            "limit": limit,
            "proxima_pagina_offset": offset + limit if offset + limit < total else None,
            "fila": queue[offset:offset + limit],
            "resumo_por_estado": state_summary,
            "nota_metodologica": (
                "A fila identifica lacunas cadastrais, não ausência de serviços no território. "
                "Prioridade alta significa necessidade de pesquisa documental, não risco ou "
                "urgência para as mulheres. Referências estaduais/nacionais não comprovam "
                "unidade local. Nenhum serviço é recomendado até validação de fonte, contato, "
                "gratuidade e condições de atendimento."
            ),
        }
