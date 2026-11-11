"""Primitivas de HTTP defensivo para conectores com destinos fixos."""

from __future__ import annotations

import json
from typing import Any

import httpx


MAX_JSON_RESPONSE_BYTES = 5 * 1024 * 1024


class UnsafeUpstreamResponse(RuntimeError):
    """Resposta externa excede os limites ou tenta redirecionar o conector."""


async def get_json(
    *,
    client: httpx.AsyncClient | None,
    url: str,
    timeout: httpx.Timeout,
    params: dict[str, Any] | None = None,
    max_bytes: int = MAX_JSON_RESPONSE_BYTES,
) -> Any:
    """Executa GET sem seguir redirects e limita bytes antes de interpretar JSON.

    Os conectores devem construir `url` exclusivamente a partir de hosts fixos
    e caminhos/parâmetros validados. Nunca passar URL fornecida pela usuária.
    """
    if not isinstance(url, str) or not url.startswith("https://"):
        raise UnsafeUpstreamResponse("Conexão externa bloqueada: HTTPS obrigatório.")
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError("max_bytes deve ser um inteiro positivo.")

    async def _request(http: httpx.AsyncClient) -> Any:
        response = await http.get(
            url,
            params=params,
            timeout=timeout,
            follow_redirects=False,
        )
        if 300 <= response.status_code < 400:
            raise UnsafeUpstreamResponse("Redirecionamento externo bloqueado.")
        response.raise_for_status()
        content_length = response.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > max_bytes:
                    raise UnsafeUpstreamResponse("Resposta externa excede o limite permitido.")
            except ValueError as exc:
                raise UnsafeUpstreamResponse("Cabeçalho de tamanho externo inválido.") from exc
        body = response.content
        if len(body) > max_bytes:
            raise UnsafeUpstreamResponse("Resposta externa excede o limite permitido.")
        content_type = response.headers.get("content-type", "").lower()
        if content_type and "json" not in content_type:
            raise UnsafeUpstreamResponse("A fonte externa não retornou conteúdo JSON.")
        try:
            return json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise UnsafeUpstreamResponse("A fonte externa retornou JSON inválido.") from exc

    if client is not None:
        return await _request(client)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as owned_client:
        return await _request(owned_client)
