"""Orquestra a resolução territorial do IBGE com a busca de estabelecimentos CNES."""
from __future__ import annotations
import unicodedata
from typing import Any
from elas_conectadas_mcp.connectors.demas import DEMASConnector
from elas_conectadas_mcp.connectors.ibge import IBGEConnector

def _normalize_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))

class HealthSearchService:
    """Resolve município/UF no IBGE e consulta registros CNES."""
    def __init__(self, ibge: IBGEConnector | None = None, demas: DEMASConnector | None = None) -> None:
        self.ibge = ibge or IBGEConnector()
        self.demas = demas or DEMASConnector()

    async def search_by_municipality(self, municipality: str, uf: str, *, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        """Resolve município no IBGE e consulta estabelecimentos ativos no DEMAS/CNES.

        O IBGE retorna código municipal de sete dígitos. A consulta CNES usa o
        código sem o dígito verificador (seis primeiros dígitos).
        """
        municipality = municipality.strip()
        uf = uf.strip().upper()
        if not municipality:
            raise ValueError("Informe o nome do município.")
        if len(uf) != 2 or not uf.isalpha():
            raise ValueError("Informe a sigla da UF com duas letras.")
        candidates = await self.ibge.list_municipalities(uf)
        wanted = _normalize_name(municipality)
        matches = [item for item in candidates if _normalize_name(str(item.get("nome", ""))) == wanted]
        if not matches:
            raise ValueError("Município não encontrado na UF informada. Confira o nome e a sigla do estado.")
        if len(matches) > 1:
            raise ValueError("Mais de um município encontrado. Informe o nome oficial completo.")
        ibge_code = int(matches[0]["id"])
        ibge_code_text = str(ibge_code)
        if len(ibge_code_text) != 7:
            raise ValueError("O IBGE retornou um código municipal fora do formato esperado.")
        cnes_municipality_code = int(ibge_code_text[:6])
        result = await self.demas.search_establishments(municipality_code=cnes_municipality_code, status=1, limit=limit, offset=offset)
        return {
            "municipality": matches[0]["nome"],
            "uf": uf,
            "ibge_municipality_code": ibge_code,
            "cnes_municipality_code": cnes_municipality_code,
            "source_ibge": "https://servicodados.ibge.gov.br/api/docs/localidades",
            "source_cnes": "https://apidadosabertos.saude.gov.br/static/swagger.json",
            "results": result,
            "important_notice": "Os resultados são registros cadastrais ativos no CNES. Não confirmam agenda, atendimento atual, gratuidade nem realização de exame específico. Confirme com a unidade ou Secretaria de Saúde.",
        }
