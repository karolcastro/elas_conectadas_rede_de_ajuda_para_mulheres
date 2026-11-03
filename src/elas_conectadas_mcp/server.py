"""Servidor MCP inicial do Elas Conectadas.

Disponibiliza tools, resources e prompts para consultas territoriais do IBGE.
"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from elas_conectadas_mcp.connectors.ibge import IBGEConnector

mcp = FastMCP(
    "Elas Conectadas",
    instructions=(
        "Você apoia mulheres a encontrar serviços confiáveis. Use fontes verificáveis, "
        "não invente serviços, contatos, gratuidade ou disponibilidade. As ferramentas "
        "deste servidor consultam somente referências territoriais do IBGE; elas não "
        "localizam unidades de saúde nem confirmam exames."
    ),
)

ibge = IBGEConnector()


@mcp.tool()
async def listar_estados() -> list[dict]:
    """Lista estados brasileiros usando a API oficial de Localidades do IBGE."""
    return await ibge.list_states()


@mcp.tool()
async def listar_municipios(uf: str) -> list[dict]:
    """Lista municípios de uma UF (sigla de duas letras), consultando o IBGE."""
    return await ibge.list_municipalities(uf)


@mcp.tool()
async def consultar_municipio(codigo_ibge: int) -> dict:
    """Consulta município pelo código IBGE e retorna município, UF e região."""
    return await ibge.get_municipality(codigo_ibge)


@mcp.resource("ibge://estados")
async def recurso_estados() -> str:
    """Resource com a lista atual de estados brasileiros."""
    return json.dumps(await ibge.list_states(), ensure_ascii=False)


@mcp.prompt()
def orientar_busca_por_municipio() -> str:
    """Instruções para usar referências territoriais na busca local."""
    return (
        "Use as ferramentas do IBGE para padronizar UF e município. "
        "Esses dados não comprovam a existência, gratuidade ou disponibilidade de "
        "qualquer serviço. Para recomendar um serviço, consulte também a fonte oficial "
        "da instituição responsável e informe a data da verificação."
    )


def main() -> None:
    """Inicia o servidor MCP pelo transporte stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
