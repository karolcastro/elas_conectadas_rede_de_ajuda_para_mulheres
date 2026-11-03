"""Servidor MCP do Elas Conectadas com conectores territoriais e de saúde."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from elas_conectadas_mcp.connectors.demas import DEMASConnector
from elas_conectadas_mcp.connectors.ibge import IBGEConnector
from elas_conectadas_mcp.connectors.viacep import ViaCEPConnector
from elas_conectadas_mcp.services.health_search import HealthSearchService
from elas_conectadas_mcp.services.menstrual_dignity import MenstrualDignityGuide
from elas_conectadas_mcp.services.official_network_directory import OfficialNetworkDirectory
from elas_conectadas_mcp.services.protection_registry import ProtectionRegistry

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
viacep = ViaCEPConnector()
health_search = HealthSearchService(ibge=ibge, demas=demas, viacep=viacep)
protection_registry = ProtectionRegistry()
official_network_directory = OfficialNetworkDirectory()
menstrual_dignity_guide = MenstrualDignityGuide()


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


@mcp.tool()
async def buscar_unidades_saude_por_cep(cep: str, limite: int = 20, pagina: int = 0) -> dict:
    """Resolve CEP pelo ViaCEP e busca estabelecimentos CNES no município identificado.

    ViaCEP é um serviço público de terceiros, não uma API oficial do Governo Federal.
    A consulta localiza o município, mas não calcula distância exata entre endereço e unidade.
    """
    return await health_search.search_by_cep(cep, limit=limite, offset=pagina)





@mcp.tool()
def listar_canais_oficiais_de_ajuda(categoria: str | None = None, uf: str | None = None) -> dict:
    """Lista canais nacionais e serviços cadastrados com fonte oficial e abrangência."""
    return protection_registry.list_services(category=categoria, uf=uf)


@mcp.tool()
def consultar_telefones_de_urgencia() -> dict:
    """Retorna canais nacionais oficiais: 190 para emergência e 180 para atendimento à mulher."""
    return protection_registry.national_emergency_channels()


@mcp.resource("protecao://fontes-e-canais")
def recurso_canais_protecao() -> str:
    """Resource com canais nacionais oficiais e catálogo validado de proteção."""
    return json.dumps(protection_registry.national_emergency_channels(), ensure_ascii=False)


@mcp.prompt()
def orientar_busca_protecao_mulher() -> str:
    """Orientação MCP para pesquisas seguras de proteção e acolhimento."""
    return (
        "Em perigo imediato, informe 190. Para orientação sobre violência contra a mulher, "
        "informe 180. Consulte o catálogo curado e nunca invente delegacias, ONGs, abrigos, "
        "advogados, endereços ou telefones. Não divulgue endereços de abrigos sigilosos. "
        "Só apresente gratuidade, horários, critérios e disponibilidade quando confirmados "
        "em fonte oficial recente; informe a fonte e a data da verificação."
    )



@mcp.tool()
def orientar_consulta_rede_oficial_atendimento(uf: str | None = None, municipio: str | None = None, tipo_servico: str | None = None) -> dict:
    """Fornece o link e instruções para consultar o Painel oficial da Rede de Atendimento.

    Não retorna unidades automaticamente: a consulta estruturada do painel não está
    disponível por API pública documentada nesta implementação.
    """
    return official_network_directory.guide(uf=uf, municipality=municipio, category=tipo_servico)


@mcp.resource("protecao://painel-rede-atendimento")
def recurso_painel_rede_atendimento() -> str:
    """Resource com o link oficial e os tipos de serviços da Rede de Atendimento."""
    return json.dumps(official_network_directory.guide(), ensure_ascii=False)


@mcp.prompt()
def orientar_acesso_rede_atendimento() -> str:
    """Prompt para orientar a consulta segura do painel oficial."""
    return (
        "Use o Painel da Rede de Atendimento do Ministério das Mulheres para consultar "
        "serviços por estado e município. Não afirme ter consultado unidades automaticamente "
        "se os registros não foram retornados por uma integração verificável. Confirme contato "
        "e funcionamento antes do deslocamento. Nunca divulgue endereços sigilosos de abrigos; "
        "nesses casos, oriente a mulher a buscar encaminhamento seguro pelo Ligue 180."
    )



@mcp.tool()
def consultar_programa_dignidade_menstrual() -> dict:
    """Explica critérios e etapas oficiais para obter absorventes gratuitos."""
    return menstrual_dignity_guide.get_guidance()


@mcp.resource("saude://dignidade-menstrual")
def recurso_dignidade_menstrual() -> str:
    """Resource com orientações oficiais do Programa Dignidade Menstrual."""
    return json.dumps(menstrual_dignity_guide.get_guidance(), ensure_ascii=False)


@mcp.prompt()
def orientar_acesso_absorventes_gratuitos() -> str:
    """Prompt de orientação sobre acesso ao Programa Dignidade Menstrual."""
    return (
        "Explique o Programa Dignidade Menstrual com base nas fontes oficiais retornadas. "
        "Não peça CPF, senha, conta gov.br nem dados sensíveis no chat. Informe que a consulta "
        "no Elas Conectadas é sem cadastro, mas o serviço externo pode exigir autenticação "
        "gov.br para emitir autorização. Não garanta estoque em farmácia; indique confirmação "
        "com a unidade e apoio de UBS/CRAS/CREAS quando necessário."
    )



@mcp.resource("seguranca://privacidade-e-dados")
def recurso_privacidade_dados() -> str:
    """Explica a minimização de dados e os limites de privacidade da versão atual."""
    return json.dumps(
        {
            "principles": [
                "Não solicitar cadastro, login, e-mail, senha, CPF ou relato detalhado para fornecer informações públicas.",
                "Solicitar apenas município/UF sempre que isso for suficiente; CEP é opcional.",
                "A consulta por CEP transmite o CEP ao ViaCEP para resolução territorial.",
                "O conector ViaCEP não persiste nem devolve CEP, logradouro ou bairro.",
                "Não coletar localização precisa do dispositivo sem consentimento explícito.",
                "Não armazenar relatos de violência, dados de saúde ou identificação pessoal sem necessidade e base legal.",
                "Nunca publicar endereço de abrigo sigiloso nem dados de beneficiárias.",
                "Não inserir dados pessoais em logs, prompts de depuração ou ferramentas de terceiros.",
            ],
            "current_runtime": "Servidor MCP local via stdio; não há banco de dados nem armazenamento de conversas implementado neste repositório.",
            "external_services": [
                "ViaCEP recebe o CEP quando a usuária escolhe a busca por CEP.",
                "IBGE recebe a consulta de município/UF.",
                "DEMAS/CNES recebe filtros territoriais para localizar cadastros de estabelecimentos.",
            ],
            "security_contact_rule": "Se houver risco de monitoramento, oferecer orientação digital segura e não presumir que navegação privada apaga rastros.",
        },
        ensure_ascii=False,
    )


@mcp.prompt()
def orientar_privacidade_e_seguranca() -> str:
    """Instruções obrigatórias de privacidade para todas as consultas."""
    return (
        "Aplique minimização de dados: prefira município/UF; peça CEP somente se necessário "
        "e explique que ele será consultado no ViaCEP. Nunca peça senha, CPF, login, e-mail, "
        "relato detalhado ou localização precisa sem necessidade e consentimento. Não registre "
        "dados pessoais em logs. Nunca exponha endereço de abrigo sigiloso. Se houver risco "
        "imediato, informe 190; para orientação sobre violência contra a mulher, 180. "
        "Se houver suspeita de monitoramento, ofereça opções de segurança sem prometer "
        "que navegação privada elimina rastros."
    )



@mcp.resource("seguranca://privacidade-e-dados")
def recurso_privacidade_dados() -> str:
    """Explica a minimização de dados e os limites de privacidade da versão atual."""
    return json.dumps(
        {
            "principles": [
                "Não solicitar cadastro, login, e-mail, senha, CPF ou relato detalhado para fornecer informações públicas.",
                "Solicitar apenas município/UF sempre que isso for suficiente; CEP é opcional.",
                "A consulta por CEP transmite o CEP ao ViaCEP para resolução territorial.",
                "O conector ViaCEP não persiste nem devolve CEP, logradouro ou bairro.",
                "Não coletar localização precisa do dispositivo sem consentimento explícito.",
                "Não armazenar relatos de violência, dados de saúde ou identificação pessoal sem necessidade e base legal.",
                "Nunca publicar endereço de abrigo sigiloso nem dados de beneficiárias.",
                "Não inserir dados pessoais em logs, prompts de depuração ou ferramentas de terceiros.",
            ],
            "current_runtime": "Servidor MCP local via stdio; não há banco de dados nem armazenamento de conversas implementado neste repositório.",
            "external_services": [
                "ViaCEP recebe o CEP quando a usuária escolhe a busca por CEP.",
                "IBGE recebe a consulta de município/UF.",
                "DEMAS/CNES recebe filtros territoriais para localizar cadastros de estabelecimentos.",
            ],
            "security_contact_rule": "Se houver risco de monitoramento, oferecer orientação digital segura e não presumir que navegação privada apaga rastros.",
        },
        ensure_ascii=False,
    )


@mcp.prompt()
def orientar_privacidade_e_seguranca() -> str:
    """Instruções obrigatórias de privacidade para todas as consultas."""
    return (
        "Aplique minimização de dados: prefira município/UF; peça CEP somente se necessário "
        "e explique que ele será consultado no ViaCEP. Nunca peça senha, CPF, login, e-mail, "
        "relato detalhado ou localização precisa sem necessidade e consentimento. Não registre "
        "dados pessoais em logs. Nunca exponha endereço de abrigo sigiloso. Se houver risco "
        "imediato, informe 190; para orientação sobre violência contra a mulher, 180. "
        "Se houver suspeita de monitoramento, ofereça opções de segurança sem prometer "
        "que navegação privada elimina rastros."
    )


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
            "api": "https://apidadosabertos.saude.gov.br",
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
