"""Servidor MCP do Elas Conectadas com conectores territoriais e de saúde."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from elas_conectadas_mcp.connectors.demas import DEMASConnector
from elas_conectadas_mcp.connectors.ibge import IBGEConnector
from elas_conectadas_mcp.connectors.viacep import ViaCEPConnector
from elas_conectadas_mcp.services.free_legal_aid import FreeLegalAidDirectory
from elas_conectadas_mcp.services.health_search import HealthSearchService
from elas_conectadas_mcp.services.menstrual_dignity import MenstrualDignityGuide
from elas_conectadas_mcp.services.official_network_directory import OfficialNetworkDirectory
from elas_conectadas_mcp.services.protection_registry import ProtectionRegistry
from elas_conectadas_mcp.services.women_economic_autonomy import WomenEconomicAutonomyDirectory
from elas_conectadas_mcp.services.women_organizations import WomenOrganizationsGuide
from elas_conectadas_mcp.services.women_training import WomenTrainingDirectory

mcp = FastMCP(
    "Elas Conectadas",
    instructions=(
        "Você apoia mulheres a encontrar serviços confiáveis com acolhimento, respeito e sem julgamento. "
        "Na primeira resposta, informe de forma visível: perigo imediato, Polícia Militar 190; "
        "orientação e atendimento sobre violência contra a mulher, Ligue 180 (gratuito, 24 horas). "
        "Comece perguntando qual idioma a mulher prefere; para não atrasar a ajuda, siga em português "
        "até que ela escolha outro idioma. Nunca condicione informações a cadastro, login, e-mail, "
        "senha, CPF ou relato detalhado. Solicite apenas a localização mínima necessária e ofereça "
        "município/UF como alternativa ao CEP. Use fontes verificáveis, não invente serviços, contatos, "
        "gratuidade, critérios ou disponibilidade. Quando free for null ou cost_status indicar custo não confirmado, nunca classifique nem recomende o registro como gratuito; apresente-o apenas como referência pendente de confirmação, se necessário. Priorize registros com free=true. Não infira gratuidade para as Casas da Mulher Brasileira a partir da gratuidade do Ligue 180. Diferencie serviços confirmados de fontes de descoberta "
        "e informe limites de cobertura e data de verificação. Nunca divulgue endereços sigilosos de abrigos; "
        "oriente encaminhamento seguro pelo Ligue 180. IBGE fornece referências territoriais. "
        "DEMAS/CNES fornece dados cadastrais de estabelecimentos; isso não confirma agenda, atendimento "
        "atual, gratuidade ou realização de exames específicos."
    ),
)

ibge = IBGEConnector()
demas = DEMASConnector()
viacep = ViaCEPConnector()
health_search = HealthSearchService(ibge=ibge, demas=demas, viacep=viacep)
protection_registry = ProtectionRegistry()
official_network_directory = OfficialNetworkDirectory()
menstrual_dignity_guide = MenstrualDignityGuide()
free_legal_aid_directory = FreeLegalAidDirectory()
women_organizations_guide = WomenOrganizationsGuide()
women_training_directory = WomenTrainingDirectory()
women_economic_autonomy_directory = WomenEconomicAutonomyDirectory()


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


@mcp.tool()
def buscar_servicos_protecao_por_localidade(
    uf: str, municipio: str | None = None, categoria: str | None = None,
    incluir_registros_vencidos: bool = False,
) -> dict:
    """Busca serviços regionais e referências oficiais por UF, município e categoria.

    Priorize free=true. Registros com free=null têm custo não confirmado e não podem ser apresentados como gratuitos.
    Não calcula distância. Por padrão, oculta registros sem verificação válida ou com revisão vencida.
    Para auditoria, incluir_registros_vencidos=True mostra registros sinalizados como expirados.
    """
    return protection_registry.list_services(
        uf=uf, municipality=municipio, category=categoria,
        include_stale=incluir_registros_vencidos,
    )


@mcp.resource("protecao://catalogo-regional")
def recurso_catalogo_regional() -> str:
    """Resource de leitura do catálogo regional validado."""
    return json.dumps(
        protection_registry.list_services(uf="SP", municipality="São Paulo"),
        ensure_ascii=False,
    )


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
        "Priorize serviços com free=true. Se free for null ou cost_status indicar custo não confirmado, não classifique o serviço como gratuito; explique a pendência e sugira confirmação direta. Só apresente gratuidade, horários, critérios e disponibilidade quando confirmados "
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




@mcp.tool()
def buscar_cursos_programas_para_mulheres(uf: str | None = None) -> dict:
    """Lista cursos gratuitos e programas destinados a mulheres, com status de inscrição e fontes."""
    return women_training_directory.search(uf=uf)


@mcp.tool()
def buscar_iniciativas_mulheres_negras_indigenas(
    uf: str | None = None,
    publico: str | None = None,
    tipo: str | None = None,
    incluir_encerradas: bool = True,
) -> dict:
    """Busca editais, bolsas, formação e iniciativas para mulheres negras, indígenas e coletivos.

    Filtros de público: negras, indigenas, quilombolas, coletivos,
    empreendedoras, vulnerabilidade_social.
    Filtros de tipo: financiamento, capacitacao, fortalecimento_coletivo, articulacao.
    Diferencia chamadas abertas, apoios restritos a turmas selecionadas e editais encerrados.
    """
    return women_economic_autonomy_directory.search(
        uf=uf, publico=publico, tipo=tipo, incluir_encerradas=incluir_encerradas
    )


@mcp.resource("autonomia://mulheres-negras-indigenas")
def recurso_iniciativas_mulheres_negras_indigenas() -> str:
    """Resource com iniciativas verificadas de autonomia econômica e fortalecimento coletivo."""
    return json.dumps(women_economic_autonomy_directory.search(), ensure_ascii=False)


@mcp.prompt()
def orientar_busca_fomento_mulheres_negras_indigenas() -> str:
    """Prompt para localizar fomento sem confundir empréstimo com apoio não reembolsável."""
    return (
        "Priorize iniciativas e editais para mulheres negras, indígenas e quilombolas, "
        "especialmente organizações e coletivos em situação de vulnerabilidade. Diferencie "
        "bolsa-prêmio, doação, capital semente, apoio institucional e empréstimo. Nunca chame "
        "crédito de recurso não reembolsável. Mostre critérios, território, prazo e fonte oficial. "
        "Se a chamada estiver encerrada, informe isso claramente e indique monitoramento de nova "
        "edição. Não solicite cadastro, login, CPF, e-mail, senha ou dados pessoais para apresentar "
        "informações públicas."
    )


@mcp.resource("capacitacao://programas-gratuitos")
def recurso_programas_gratuitos_mulheres() -> str:
    """Resource de cursos e programas gratuitos com público e status transparentes."""
    return json.dumps(women_training_directory.search(), ensure_ascii=False)


@mcp.prompt()
def orientar_inscricao_cursos_mulheres() -> str:
    """Prompt para orientar cursos sem pedir credenciais ou prometer vagas."""
    return (
        "Priorize cursos gratuitos criados por mulheres para mulheres ou destinados especificamente "
        "a mulheres. Mostre público-alvo, formato, fonte oficial, data de verificação e status real. "
        "Não transforme curso listado em inscrição aberta nem anuncie vagas sem confirmação atual. "
        "Se o portal externo exigir gov.br, oriente a usuária a acessar diretamente o site oficial; "
        "nunca peça CPF, senha, login, e-mail ou documentos no chat."
    )



@mcp.tool()
def orientar_assistencia_juridica_gratuita(
    uf: str | None = None, municipio: str | None = None
) -> dict:
    """Orienta como localizar Defensoria Pública e assistência jurídica gratuita oficial."""
    return free_legal_aid_directory.guide(uf=uf, municipality=municipio)


@mcp.resource("juridico://assistencia-gratuita")
def recurso_assistencia_juridica_gratuita() -> str:
    """Resource com diretórios oficiais de assistência jurídica gratuita."""
    return json.dumps(free_legal_aid_directory.guide(), ensure_ascii=False)


@mcp.prompt()
def orientar_busca_defensoria_mulher() -> str:
    """Prompt para localizar assistência jurídica sem solicitar dados pessoais."""
    return (
        "Ajude a localizar a Defensoria Pública e serviços jurídicos gratuitos usando "
        "fontes institucionais. Informe critérios e agendamento conforme a fonte do estado. "
        "Em São Paulo, informe o telefone 0800 773 4340 e o horário publicado, esclarecendo "
        "que o atendimento requer agendamento. Não solicite CPF, senha, login, e-mail, "
        "documentos ou relato detalhado no chat. Não prometa elegibilidade nem resultado jurídico."
    )



@mcp.tool()
def orientar_acesso_creas(uf: str | None = None, municipio: str | None = None) -> dict:
    """Orienta acesso gratuito ao CREAS e localizador oficial do MDS."""
    return free_legal_aid_directory.creas_guide(uf=uf, municipality=municipio)


@mcp.resource("assistencia://creas")
def recurso_acesso_creas() -> str:
    """Resource com informações oficiais sobre o CREAS e acesso gratuito."""
    return json.dumps(free_legal_aid_directory.creas_guide(), ensure_ascii=False)


@mcp.prompt()
def orientar_busca_apoio_psicossocial() -> str:
    """Prompt para orientar acesso ao CREAS sem prometer vaga ou atendimento."""
    return (
        "Oriente a mulher a localizar o CREAS pelo localizador oficial do MDS. "
        "Explique que é um serviço público e gratuito para pessoas e famílias com direitos violados, "
        "incluindo violência física, psicológica e sexual. Se não houver CREAS no município, "
        "oriente procurar a assistência social da prefeitura. Não invente endereço, horário, vaga "
        "ou disponibilidade e não solicite documentos, CPF ou relato detalhado no chat."
    )


@mcp.tool()
def orientar_acesso_cras(uf: str | None = None, municipio: str | None = None) -> dict:
    """Orienta acesso gratuito ao CRAS, proteção social básica e Cadastro Único."""
    return free_legal_aid_directory.cras_guide(uf=uf, municipality=municipio)


@mcp.resource("assistencia://cras")
def recurso_acesso_cras() -> str:
    """Resource com informações oficiais sobre CRAS e Cadastro Único."""
    return json.dumps(free_legal_aid_directory.cras_guide(), ensure_ascii=False)



@mcp.tool()
def orientar_acesso_moradia_popular(uf: str | None = None, municipio: str | None = None) -> dict:
    """Explica a prioridade de mulheres no Minha Casa, Minha Vida e o acesso municipal."""
    return free_legal_aid_directory.housing_guide(uf=uf, municipality=municipio)


@mcp.resource("habitacao://minha-casa-minha-vida-mulheres")
def recurso_prioridade_habitacional_mulheres() -> str:
    """Resource com direitos e limites da prioridade habitacional para mulheres."""
    return json.dumps(free_legal_aid_directory.housing_guide(), ensure_ascii=False)



@mcp.tool()
def orientar_acesso_alimentacao_gratuita(uf: str | None = None, municipio: str | None = None) -> dict:
    """Orienta busca por cozinhas solidárias, cozinhas comunitárias e restaurantes populares."""
    return free_legal_aid_directory.food_security_guide(uf=uf, municipality=municipio)


@mcp.resource("alimentacao://apoio-gratuito")
def recurso_acesso_alimentacao_gratuita() -> str:
    """Resource com opções oficiais de alimentação gratuita ou de baixo custo."""
    return json.dumps(free_legal_aid_directory.food_security_guide(), ensure_ascii=False)



@mcp.tool()
def orientar_beneficios_mulheres_vulnerabilidade(
    uf: str | None = None, municipio: str | None = None
) -> dict:
    """Orienta sobre CadÚnico, Bolsa Família, BPC, Auxílio-Inclusão, Centro POP e acolhimento."""
    return free_legal_aid_directory.vulnerable_women_guide(uf=uf, municipality=municipio)


@mcp.resource("assistencia://beneficios-mulheres-vulnerabilidade")
def recurso_beneficios_mulheres_vulnerabilidade() -> str:
    """Resource nacional sobre benefícios e proteção social para mulheres vulneráveis."""
    return json.dumps(free_legal_aid_directory.vulnerable_women_guide(), ensure_ascii=False)


@mcp.tool()
def orientar_busca_ongs_coletivos_mulheres(
    uf: str | None = None, municipio: str | None = None
) -> dict:
    """Indica fontes públicas para descobrir e validar ONGs e coletivos de mulheres."""
    return women_organizations_guide.guide(uf=uf, municipality=municipio)


@mcp.resource("comunidade://ongs-e-coletivos")
def recurso_ongs_coletivos_mulheres() -> str:
    """Resource com fontes de descoberta e critérios de validação de iniciativas."""
    return json.dumps(women_organizations_guide.guide(), ensure_ascii=False)


@mcp.prompt()
def orientar_validacao_ong_feminina() -> str:
    """Prompt para validar iniciativas sem inventar organizações ou serviços."""
    return (
        "Use fontes institucionais para descobrir e validar ONGs, coletivos e iniciativas "
        "femininas. O Mapa das OSC é fonte de descoberta, não prova atendimento atual, "
        "gratuidade ou liderança feminina. Confirme atuação local, público, custo, horários, "
        "contato e status antes de recomendar. Não invente organizações e não solicite cadastro "
        "ou dados pessoais para apresentar informações públicas."
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
