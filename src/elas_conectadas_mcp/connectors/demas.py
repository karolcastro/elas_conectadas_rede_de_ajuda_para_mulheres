"""Conector para a API DEMAS/CNES do Ministério da Saúde.

Swagger oficial: https://apidadosabertos.saude.gov.br/static/swagger.json
API pública, sem autenticação segundo a página institucional do Ministério da Saúde.
Os registros CNES não confirmam agenda, gratuidade, atendimento ou disponibilidade de exames.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

BASE_URL = "https://apidadosabertos.saude.gov.br"
SOURCE_URL = "https://apidadosabertos.saude.gov.br/"
SWAGGER_URL = "https://apidadosabertos.saude.gov.br/static/swagger.json"
_TIMEOUT = httpx.Timeout(25.0, connect=7.0)


class DEMASAPIError(RuntimeError):
    """Falha ao consultar ou interpretar a API DEMAS."""


def _positive_int(value: int, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field} deve ser um inteiro positivo.")
    return value


def _pagination(limit: int, offset: int, maximum: int = 1000) -> tuple[int, int]:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= maximum:
        raise ValueError(f"limit deve estar entre 1 e {maximum}.")
    if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
        raise ValueError("offset deve ser um inteiro maior ou igual a zero.")
    return limit, offset


def _records(payload: Any) -> list[dict[str, Any]]:
    """Aceita formatos JSON comuns sem presumir nomes de campos não documentados."""
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("data", "dados", "results", "resultados", "items", "registros"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    raise DEMASAPIError("A API DEMAS retornou um formato JSON não reconhecido.")


class DEMASConnector:
    """Consulta estabelecimentos e UBS cadastrados no CNES."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def _get(self, path: str, params: dict[str, Any]) -> Any:
        url = f"{BASE_URL}/{path.lstrip('/')}"
        try:
            if self._client is not None:
                response = await self._client.get(url, params=params, timeout=_TIMEOUT)
            else:
                async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                    response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise DEMASAPIError(
                "Não foi possível consultar a base pública DEMAS/CNES neste momento."
            ) from exc

    @staticmethod
    def _with_provenance(records: list[dict[str, Any]], endpoint: str) -> dict[str, Any]:
        return {
            "source": "Ministério da Saúde — DEMAS / CNES",
            "source_url": SOURCE_URL,
            "api_endpoint": f"{BASE_URL}/{endpoint}",
            "documentation_url": SWAGGER_URL,
            "checked_at": datetime.now(UTC).isoformat(),
            "record_count": len(records),
            "records": records,
            "important_notice": (
                "Cadastro CNES identifica dados registrados do estabelecimento. "
                "Não confirma agenda, atendimento atual, gratuidade nem realização "
                "de exame específico. Esses dados devem ser confirmados com a unidade "
                "ou Secretaria de Saúde responsável."
            ),
        }

    async def search_establishments(
        self,
        *,
        municipality_code: int | None = None,
        state_code: int | None = None,
        unit_type_code: int | None = None,
        status: int = 1,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Pesquisa estabelecimentos por códigos oficiais e status CNES.

        O Swagger do endpoint informa filtros por código municipal, UF, tipo e status.
        A documentação desse endpoint descreve limit <= 20; usamos esse teto conservador.
        """
        params: dict[str, Any] = {}
        if municipality_code is not None:
            params["codigo_municipio"] = _positive_int(municipality_code, "municipality_code")
        if state_code is not None:
            params["codigo_uf"] = _positive_int(state_code, "state_code")
        if unit_type_code is not None:
            params["codigo_tipo_unidade"] = _positive_int(unit_type_code, "unit_type_code")
        if status not in (0, 1) or isinstance(status, bool):
            raise ValueError("status deve ser 1 (ativo) ou 0 (inativo).")
        params["status"] = status
        limit, offset = _pagination(limit, offset, maximum=20)
        params.update({"limit": limit, "offset": offset})
        endpoint = "cnes/estabelecimentos"
        records = _records(await self._get(endpoint, params))
        return self._with_provenance(records, endpoint)

    async def get_establishment(self, cnes_code: int) -> dict[str, Any]:
        """Consulta um estabelecimento pelo código CNES."""
        code = _positive_int(cnes_code, "cnes_code")
        endpoint = f"cnes/estabelecimentos/{code}"
        payload = await self._get(endpoint, {})
        if not isinstance(payload, dict):
            raise DEMASAPIError("A API DEMAS retornou um formato inesperado para o estabelecimento.")
        return self._with_provenance([payload], endpoint)

    async def list_basic_health_units(
        self, *, limit: int = 100, offset: int = 0
    ) -> dict[str, Any]:
        """Lista UBS cadastradas no CNES; endpoint documenta paginação até 1000."""
        limit, offset = _pagination(limit, offset, maximum=1000)
        endpoint = "assistencia-a-saude/unidade-basicas-de-saude"
        records = _records(await self._get(endpoint, {"limit": limit, "offset": offset}))
        return self._with_provenance(records, endpoint)
