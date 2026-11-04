"""Conector público de CEP via ViaCEP, sem autenticação."""
from __future__ import annotations

import re
from typing import Any

import httpx

BASE_URL = "https://viacep.com.br/ws"
_TIMEOUT = httpx.Timeout(12.0, connect=5.0)


class ViaCEPError(RuntimeError):
    """Falha ao consultar o serviço ViaCEP."""


class ViaCEPConnector:
    """Consulta endereço e código IBGE associados a um CEP brasileiro."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def lookup(self, cep: str) -> dict[str, Any]:
        digits = re.sub(r"\D", "", cep)
        if not re.fullmatch(r"\d{8}", digits):
            raise ValueError("Informe um CEP válido com oito dígitos.")
        url = f"{BASE_URL}/{digits}/json/"
        try:
            if self._client is not None:
                response = await self._client.get(url, timeout=_TIMEOUT)
            else:
                async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                    response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ViaCEPError("Não foi possível consultar o ViaCEP neste momento.") from exc
        if not isinstance(data, dict) or data.get("erro") is True:
            raise ValueError("CEP não encontrado na base consultada.")
        ibge = data.get("ibge")
        if not ibge or not str(ibge).isdigit():
            raise ViaCEPError("O ViaCEP não retornou o código IBGE do município.")
        # Minimiza os dados devolvidos: não ecoa CEP, rua ou bairro.
        # O CEP é transmitido ao ViaCEP para resolução, mas não é persistido por este conector.
        return {
            "municipality": data.get("localidade"),
            "uf": data.get("uf"),
            "ibge_municipality_code": int(ibge),
            "source": "ViaCEP",
            "source_url": "https://viacep.com.br/",
            "privacy_notice": (
                "O CEP foi enviado ao ViaCEP para identificar município e UF. "
                "Esta implementação não armazena o CEP e não devolve rua ou bairro."
            ),
            "important_notice": (
                "O CEP identifica o município; não fornece coordenadas precisas nem "
                "comprova a proximidade física de unidades de saúde."
            ),
        }
