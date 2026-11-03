"""Servidor MCP do Elas Conectadas com conectores territoriais e de saúde."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from elas_conectadas_mcp.connectors.demas import DEMASConnector
from elas_conectadas_mcp.connectors.ibge import IBGEConnector
from elas_conectadas_mcp.services.health_search import HealthSearchService

mcp = FastMCP(
    "Elas Conectadas",
    instructions=(
        "Você apoia mulheres a encontrar serviços confiáveis. Use fontes verificáveis, "
        "não invente serviços, contatos, gratuidade ou disponibilidade. IBGE fornece "
        "referências territoriais. DEMAS/CNES fornece dados cadastrais de estabelecimentos; "
        "isso não confirma agenda, atendimento atual ou realização de exames."
    ),
)

ibge = IBGEConnector()
demas = DEMASConnector()
health_search = HealthSearchService(ibge=ibge, demas=demas)


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


@mcp.tool()
async def buscar_estabelecimentos_saude(
    codigo_municipio: int | None = None,
    codigo_uf: int | None = None,
    codigo_tipo_unidade: int | None = None,
    status: int = 1,
    limite: int = 20,
    pagina: int = 0,
) -> dict:
    """Busca estabelecimentos CNES por código IBGE municipal/UF, tipo e status.

    Retorna dados cadastrais da API DEMAS. Não confirma agenda, gratuidade,
    atendimento atual ou realização de exame específico.
    """
    return await demas.search_establishments(
        municipality_code=codigo_municipio,
        state_code=codigo_uf,
        unit_type_code=codigo_tipo_unidade,
        status=status,
        limit=limite,
        offset=pagina,
    )


@mcp.tool()
async def consultar_estabelecimento_cnes(codigo_cnes: int) -> dict:
    """Consulta dados cadastrais de um estabelecimento pelo código CNES."""
    return await demas.get_establishment(codigo_cnes)


@mcp.tool()
async def listar_ubs_cnes(limite: int = 100, pagina: int = 0) -> dict:
    """Lista UBS cadastradas no CNES com paginação (limite máximo documentado: 1000)."""
    return await demas.list_basic_health_units(limit=limite, offset=pagina)


@mcp.tool()
async def buscar_unidades_saude_por_municipio(municipio: str, uf: str, limite: int = 20, pagina: int = 0) -> dict:
    """Resolve município/UF no IBGE e busca estabelecimentos ativos no CNES/DEMAS."""
    return await health_search.search_by_municipality(municipality=municipio, uf=uf, limit=limite, offset=pagina)


@mcp.resource("ibge://estados")
async def recurso_estados() -> str:
    """Resource com a lista atual de estados brasileiros."""
    return json.dumps(await ibge.list_states(), ensure_ascii=False)


@mcp.resource("demas://fontes")
def recurso_fontes_demas() -> str:
    """Resource com referências oficiais e limites da fonte DEMAS/CNES."""
    return json.dumps(
        {
            "source": "Ministério da Saúde — DEMAS / CNES",
            "api": "https://apidadosabertos.saude.gov.br/v1",
            "swagger": "https://apidadosabertos.saude.gov.br/static/swagger.json",
            "access": "API pública sem autenticação, conforme página institucional do MS",
            "limitations": [
                "Dados cadastrais não confirmam agenda ou disponibilidade.",
                "Cadastro de estabelecimento não comprova realização de exame específico.",
                "Gratuidade e critérios de acesso devem ser confirmados com a unidade/gestor.",
            ],
        },
        ensure_ascii=False,
    )


@mcp.prompt()
def orientar_busca_por_municipio() -> str:
    """Instruções para usar referências territoriais na busca local."""
    return (
        "Use as ferramentas do IBGE para padronizar UF e município. "
        "Use DEMAS/CNES para localizar registros cadastrais de estabelecimentos. "
        "Esses dados não comprovam agenda, gratuidade ou disponibilidade de exames. "
        "Para recomendar um serviço, consulte também a fonte oficial da instituição "
        "responsável e informe a data da verificação."
    )


def main() -> None:
    """Inicia o servidor MCP pelo transporte stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
