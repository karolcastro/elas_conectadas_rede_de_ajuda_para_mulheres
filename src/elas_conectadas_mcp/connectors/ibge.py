"""Conector assíncrono para a API oficial de Localidades do IBGE.

Documentação: https://servicodados.ibge.gov.br/api/docs/localidades
Este conector trata apenas de referências territoriais; não localiza serviços de saúde.
"""

from __future__ import annotations

import re
from typing import Any

import httpx

BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
_TIMEOUT = httpx.Timeout(15.0, connect=5.0)


class IBGEAPIError(RuntimeError):
    """Erro ao consultar ou interpretar a API de Localidades do IBGE."""


def _validate_uf(uf: str) -> str:
    value = uf.strip().upper()
    if not re.fullmatch(r"[A-Z]{2}", value):
        raise ValueError("Informe uma sigla de UF válida com duas letras.")
    return value


def _validate_municipality_id(municipality_id: int) -> int:
    if isinstance(municipality_id, bool) or not isinstance(municipality_id, int):
        raise ValueError("O código do município deve ser um número inteiro.")
    if municipality_id <= 0:
        raise ValueError("O código do município deve ser positivo.")
    return municipality_id


class IBGEConnector:
    """Consulta estados e municípios sem exigir chave de API."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def _get(self, path: str) -> Any:
        url = f"{BASE_URL}/{path.lstrip('/')}"
        try:
            if self._client is not None:
                response = await self._client.get(url, timeout=_TIMEOUT)
            else:
                async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                    response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise IBGEAPIError("Não foi possível consultar a API do IBGE neste momento.") from exc

    async def list_states(self) -> list[dict[str, Any]]:
        """Retorna os estados brasileiros ordenados por nome."""
        data = await self._get("estados?orderBy=nome")
        if not isinstance(data, list):
            raise IBGEAPIError("A API do IBGE retornou um formato inesperado para estados.")
        return [
            {
                "id": item.get("id"),
                "sigla": item.get("sigla"),
                "nome": item.get("nome"),
                "regiao": (item.get("regiao") or {}).get("nome"),
            }
            for item in data
            if isinstance(item, dict)
        ]

    async def list_municipalities(self, uf: str) -> list[dict[str, Any]]:
        """Retorna municípios de uma UF, validando a sigla antes da consulta."""
        state = _validate_uf(uf)
        data = await self._get(f"estados/{state}/municipios?orderBy=nome")
        if not isinstance(data, list):
            raise IBGEAPIError("A API do IBGE retornou um formato inesperado para municípios.")
        return [
            {
                "id": item.get("id"),
                "nome": item.get("nome"),
                "microrregiao": ((item.get("microrregiao") or {}).get("nome")),
            }
            for item in data
            if isinstance(item, dict)
        ]

    async def get_municipality(self, municipality_id: int) -> dict[str, Any]:
        """Retorna os dados territoriais de um município pelo código IBGE."""
        code = _validate_municipality_id(municipality_id)
        data = await self._get(f"municipios/{code}")
        if not isinstance(data, dict):
            raise IBGEAPIError("A API do IBGE retornou um formato inesperado para o município.")
        state = data.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {})
        return {
            "id": data.get("id"),
            "nome": data.get("nome"),
            "uf": state.get("sigla"),
            "estado": state.get("nome"),
            "regiao": state.get("regiao", {}).get("nome"),
        }
