"""Fontes e iniciativas verificadas de apoio gratuito a mulheres."""
from __future__ import annotations

import unicodedata
from typing import Any

IPEA_MAP_URL = "https://mapaosc.ipea.gov.br/"
MINISTRY_PANEL_URL = "https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento"
LIGUE_180_URL = "https://www.gov.br/mulheres/pt-br/ligue180"
TAMOJUNTAS_URL = "https://tamojuntas.org.br/"
TAMOJUNTAS_SERVICE_URL = "https://tamojuntas.org.br/elementor-2722/"
MAPA_ACOLHIMENTO_URL = "https://www.mapadoacolhimento.org/atendimento/"
MARIA_DAJUDA_URL = "https://mariadajuda.org/"
MARIAS_DA_INTERNET_URL = "https://www.mariasdainternet.com.br/"
SAFERNET_HELPLINE_URL = "https://new.safernet.org.br/helpline"
ACOLHE_MAIS_URL = "https://www.gov.br/saude/pt-br/assuntos/noticias/2026/outubro/precisa-de-acolhimento-em-saude-mental-saiba-como-acessar-o-acolhe-mais-pelo-meu-sus-digital"
LBV_SER_MULHER_URL = "https://www.lbv.org.br/programa-ser-mulher/"
NUMAPE_URL = "https://www.seti.pr.gov.br/numape"
VERIFICATION_DATE = "2026-11-04"

IN_PERSON_CITIES = {
    ("BA", "salvador"),
    ("PE", "recife"),
    ("SP", "sao paulo"),
    ("RJ", "rio de janeiro"),
}


def _normalize_place(value: str | None) -> str | None:
    if not value:
        return None
    normalized = unicodedata.normalize("NFKD", value.strip().casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _locality_match(
    organization: dict[str, Any], uf: str | None, municipality: str | None
) -> tuple[int, str, str]:
    name = organization["name"]
    city = _normalize_place(municipality)
    if name == "TamoJuntas":
        if uf and city and (uf, city) in IN_PERSON_CITIES:
            return (
                0,
                "presential_city_published",
                "Cidade consta na página institucional como local de atendimento presencial; confirmar disponibilidade atual.",
            )
        if uf and city:
            if organization.get("state_contact"):
                return (
                    2,
                    "state_contact_published_no_local_service_confirmation",
                    "Há e-mail institucional associado à UF, mas a cidade não consta entre as localidades de atendimento presencial publicado. A organização informa orientações e encaminhamentos para outras localidades.",
                )
            return (
                3,
                "no_local_service_confirmation",
                "Não há atendimento presencial confirmado para esta cidade nesta base. A organização informa orientações e encaminhamentos para outras localidades; consulte o contato geral.",
            )
        if uf:
            return (
                2,
                "state_contact_only_city_not_provided",
                "Há contato institucional associado à UF, mas sem município informado não é possível confirmar atendimento presencial local.",
            )
        return (
            3,
            "location_not_provided",
            "Informe município e UF para verificar se a localidade consta entre as cidades com atendimento presencial publicado.",
        )
    if name == "NUMAPE — Núcleo Maria da Penha":
        if uf == "PR":
            return (
                2,
                "statewide_regional_network",
                "A SETI/PR publica unidades e áreas de abrangência em diferentes comarcas. A cidade precisa ser comparada à área de cada unidade; não presumir atendimento em todo o Paraná.",
            )
        return (
            4,
            "state_not_covered",
            "A rede NUMAPE cadastrada nesta entrada é do Paraná; não há cobertura confirmada para a UF informada.",
        )
    if name == "Acolhe Mais — SUS":
        return (
            1,
            "national_online_scope",
            "O Ministério da Saúde informa teleatendimento gratuito em todo o Brasil. O acesso externo exige Meu SUS Digital/conta gov.br e cadastro na plataforma oficial; o Elas Conectadas não solicita essas credenciais.",
        )
    if name == "Programa Ser Mulher — LBV":
        return (
            1,
            "national_online_scope_availability_to_confirm",
            "A página institucional descreve atendimento online nacional e gratuito, mas foi publicada em 2022; confirmar se o programa está recebendo solicitações atualmente.",
        )
    if name == "Mapa do Acolhimento":
        return (
            1,
            "national_online_scope",
            "A plataforma publica critérios nacionais e atendimento por profissionais voluntárias; isso não confirma disponibilidade de profissional ou prazo na localidade.",
        )
    if name == "Maria d'Ajuda — MariaLab":
        return (
            1,
            "latin_america_online_scope",
            "A linha de ajuda informa atendimento online para a América Latina; a resposta depende da análise e disponibilidade da equipe.",
        )
    return (4, "locality_not_assessed", "Cobertura local não avaliada.")


class WomenOrganizationsGuide:
    """Apresenta iniciativas com evidência institucional e explicita limites de cobertura."""

    def guide(
        self, *, uf: str | None = None, municipality: str | None = None
    ) -> dict[str, Any]:
        if uf and (len(uf.strip()) != 2 or not uf.strip().isalpha()):
            raise ValueError("Informe a sigla da UF com duas letras.")
        if municipality and len(municipality.strip()) < 2:
            raise ValueError("Informe um município válido.")

        normalized_uf = uf.strip().upper() if uf else None
        verified_organizations = [
            {
                "name": "Acolhe Mais — SUS",
                "organization_type": "Programa público federal de teleatendimento psicológico",
                "support": [
                    "teleatendimento psicológico por videochamada",
                    "escuta e avaliação inicial de necessidades e riscos",
                    "orientação para continuidade do cuidado na rede SUS",
                ],
                "audience": (
                    "Mulheres que vivem ou viveram situações de violência e mulheres que cuidam de familiares "
                    "com deficiência, transtornos do neurodesenvolvimento ou doenças raras."
                ),
                "cost": "Gratuito, conforme Ministério da Saúde.",
                "service_modes": ["online por videochamada"],
                "territorial_scope": "Brasil; o Ministério da Saúde informa disponibilidade nacional.",
                "application_channel": ACOLHE_MAIS_URL,
                "website": "https://meususdigital.saude.gov.br/",
                "access_requirements": (
                    "O acesso externo exige conta gov.br no Meu SUS Digital e cadastro na plataforma AgSUS. "
                    "Não é necessário encaminhamento prévio nem documento que comprove violência ou condição de cuidadora."
                ),
                "access_steps": [
                    "Abrir o aplicativo Meu SUS Digital e entrar diretamente na conta gov.br.",
                    "Acessar Miniapps e selecionar Acolhe Mais — Agora Tem Especialistas em Saúde Mental para Mulheres.",
                    "Concluir o cadastro no ambiente oficial da AgSUS e aguardar o contato para agendamento.",
                ],
                "service_hours": "Segunda a sexta, 8h–20h; sábados, 8h–14h, conforme publicação do Ministério da Saúde.",
                "limitations": (
                    "A publicação informa até dez sessões por ciclo e contato da equipe em até 24 horas após o cadastro; "
                    "não prometer horário específico ou disponibilidade antes da confirmação. Não substitui emergência, "
                    "CAPS, UBS ou canais de proteção. O agente não solicita conta gov.br, senha ou dados de acesso."
                ),
                "verification_date": VERIFICATION_DATE,
                "verification_basis": "Ministério da Saúde, notícia oficial publicada em 27/10/2026 e atualizada em 28/10/2026.",
            },
            {
                "name": "NUMAPE — Núcleo Maria da Penha",
                "organization_type": "Programa público estadual em parceria com universidades estaduais do Paraná",
                "support": [
                    "acolhimento e assistência jurídica gratuita",
                    "atendimento psicológico",
                    "atendimento e orientação social",
                    "orientação sobre direitos e medidas protetivas",
                ],
                "audience": "Mulheres em situação de violência doméstica e familiar.",
                "cost": "Gratuito, conforme Secretaria da Ciência, Tecnologia e Ensino Superior do Paraná.",
                "service_modes": ["presencial nas unidades e áreas de abrangência publicadas"],
                "territorial_scope": (
                    "Paraná, por unidades vinculadas a universidades estaduais e comarcas específicas. "
                    "A cobertura deve ser verificada pela lista oficial de unidades; não é atendimento automaticamente disponível em todos os municípios."
                ),
                "website": NUMAPE_URL,
                "application_channel": NUMAPE_URL,
                "limitations": (
                    "A página estadual publica unidades, contatos e áreas de abrangência. A cidade informada deve ser "
                    "conferida na descrição da unidade; confirmar funcionamento, critérios e disponibilidade diretamente. "
                    "Não presumir atendimento remoto."
                ),
                "verification_date": VERIFICATION_DATE,
                "verification_basis": "Secretaria da Ciência, Tecnologia e Ensino Superior do Paraná — página oficial do NUMAPE e diretório de unidades.",
            },
            {
                "name": "Programa Ser Mulher — LBV",
                "organization_type": "Programa de atendimento psicoterapêutico de organização da sociedade civil",
                "support": [
                    "atendimento psicoterapêutico online",
                    "apoio a meninas e mulheres que vivenciaram violência física, psicológica, patrimonial ou moral",
                ],
                "audience": "Pessoas do gênero feminino a partir de 12 anos, com histórico de violência e acesso a aparelho com internet, conforme página institucional.",
                "cost": "Gratuito, conforme declaração da LBV.",
                "service_modes": ["online"],
                "territorial_scope": "Brasil, conforme a página institucional.",
                "contact_phone": "(11) 9999-66-557",
                "website": LBV_SER_MULHER_URL,
                "application_channel": LBV_SER_MULHER_URL,
                "limitations": (
                    "A página institucional disponível foi publicada em 24/11/2022. Embora descreva atendimento gratuito "
                    "e publique WhatsApp de contato, não confirma que o programa esteja recebendo novas solicitações em 2026. "
                    "Antes de encaminhar, confirmar diretamente se o canal e o atendimento permanecem ativos."
                ),
                "verification_date": VERIFICATION_DATE,
                "verification_basis": "Página institucional da LBV; publicação original de 24/11/2022, consultada em 04/11/2026.",
            },
            {
                "name": "TamoJuntas",
                "organization_type": "ONG feminista composta por mulheres profissionais voluntárias",
                "support": [
                    "orientação e assessoria jurídica",
                    "acolhimento e acompanhamento psicossocial",
                    "encaminhamentos e apoio social",
                ],
                "audience": "Mulheres em situação de violência e vulnerabilidade social; a organização informa atendimento a mulheres cis e trans.",
                "cost": "Gratuito, conforme declaração institucional.",
                "service_modes": ["online", "presencial em localidades com equipe"],
                "territorial_scope": (
                    "A organização informa atuação e voluntárias em diversas regiões do Brasil. "
                    "A página de atendimento identifica Salvador, Recife, São Paulo e Rio de Janeiro "
                    "como cidades com atendimento presencial; confirme a oferta atual antes de encaminhar."
                ),
                "state_contact": {
                    "BA": "contato@tamojuntas.org.br",
                    "SP": "tamojuntas.sp@tamojuntas.org.br",
                    "RJ": "tamojuntas.rj@tamojuntas.org.br",
                    "MG": "tamojuntas.mg@tamojuntas.org.br",
                    "CE": "tamojuntas.ce@tamojuntas.org.br",
                    "PE": "tamojuntas.pe@tamojuntas.org.br",
                }.get(normalized_uf),
                "general_contact": "contato@tamojuntas.org.br",
                "website": TAMOJUNTAS_URL,
                "service_page": TAMOJUNTAS_SERVICE_URL,
                "limitations": (
                    "A presença de voluntárias não comprova atendimento imediato em todo município. "
                    "A disponibilidade, modalidade, escopo profissional e possibilidade de assumir o caso "
                    "devem ser confirmados diretamente com a organização."
                ),
                "verification_date": VERIFICATION_DATE,
                "verification_basis": "Páginas institucionais Quem Somos, Nossa Atuação e Atendimento a mulheres em situação de violência.",
            },
            {
                "name": "Mapa do Acolhimento",
                "organization_type": "Plataforma de conexão com rede voluntária de profissionais",
                "support": [
                    "acolhimento psicológico",
                    "orientação e atendimento jurídico",
                ],
                "audience": (
                    "Mulheres cis ou trans, maiores de 18 anos, residentes no Brasil, "
                    "em situação de baixa renda e que passaram por violência de gênero."
                ),
                "cost": "Gratuito; a plataforma informa que os atendimentos voluntários são 100% gratuitos.",
                "service_modes": ["online"],
                "territorial_scope": "Brasil, conforme critérios publicados pela plataforma.",
                "application_channel": MAPA_ACOLHIMENTO_URL,
                "website": "https://www.mapadoacolhimento.org/",
                "limitations": (
                    "A plataforma informa critérios de elegibilidade e solicita o preenchimento de formulário "
                    "externo para pedir atendimento. Isso não é cadastro no Elas Conectadas. "
                    "O agente não deve preencher o formulário, coletar dados pessoais ou prometer "
                    "aceitação, prazo de resposta ou disponibilidade de profissional."
                ),
                "verification_date": VERIFICATION_DATE,
                "verification_basis": "Página oficial Peça ajuda no Mapa do Acolhimento.",
            },
            {
                "name": "Maria d'Ajuda — MariaLab",
                "organization_type": "Linha de ajuda em segurança digital criada por organização feminista",
                "support": [
                    "acolhimento e orientação em segurança digital",
                    "orientação em casos de perda de contas, ataques de ódio e assédio online",
                    "orientação em situações de perseguição, repressão e censura digital",
                    "estratégias de mitigação de danos em ameaças digitais",
                ],
                "audience": "Mulheres, pessoas não binárias, pessoas LGBTQIA+ e organizações da América Latina, conforme a apresentação institucional.",
                "cost": "Gratuito, conforme declaração institucional.",
                "service_modes": ["online por e-mail"],
                "territorial_scope": "América Latina; a página institucional não restringe o atendimento a um município específico.",
                "contact_email": "sos@mariadajuda.org",
                "website": MARIA_DAJUDA_URL,
                "response_time": "A página informa retorno em até 2 dias após o envio do e-mail; confirmar a condição atual diretamente com a equipe.",
                "limitations": (
                    "Atendimento especializado em segurança e cuidados digitais; não substitui emergência policial, "
                    "assistência jurídica ou atendimento psicológico. A equipe informa que encaminha para outras linhas "
                    "quando a demanda não é de segurança digital."
                ),
                "verification_date": VERIFICATION_DATE,
                "verification_basis": "Página institucional da Maria d'Ajuda/MariaLab, com declaração de gratuidade, público, escopo e canal de contato.",
            },
        ]
        for organization in verified_organizations:
            priority, match, evidence = _locality_match(
                organization, normalized_uf, municipality
            )
            organization["locality_priority"] = priority
            organization["locality_match"] = match
            organization["locality_evidence"] = evidence

        verified_organizations.sort(key=lambda item: item["locality_priority"])

        return {
            "purpose": "Descobrir organizações da sociedade civil, ONGs e iniciativas de apoio a mulheres.",
            "requested_location": {
                "uf": normalized_uf,
                "municipality": municipality.strip() if municipality else None,
            },
            "verified_organizations": verified_organizations,
            "organizations_requiring_cost_confirmation": [
                {
                    "name": "Marias da Internet",
                    "support": "Orientação jurídica, psicológica e de perícia digital para mulheres vítimas de divulgação não autorizada de imagens íntimas, conforme página institucional.",
                    "website": MARIAS_DA_INTERNET_URL,
                    "cost": "Não confirmado nas páginas institucionais consultadas. Não apresentar como gratuito até confirmação direta.",
                    "limitations": "O site disponibiliza um canal para solicitar ajuda, mas a gratuidade e a disponibilidade atual não foram confirmadas nesta verificação.",
                    "verification_date": VERIFICATION_DATE,
                }
            ],
            "scope_notes": [
                {
                    "name": "SaferNet — Helpline",
                    "note": "A página oficial informa que o Helpline atende crianças e adolescentes e que adultos não são elegíveis para orientação individual. Não recomendar como canal geral para mulheres adultas.",
                    "url": SAFERNET_HELPLINE_URL,
                }
            ],
            "discovery_sources": [
                {
                    "name": "IPEA — Mapa das Organizações da Sociedade Civil",
                    "url": IPEA_MAP_URL,
                    "scope": "Base pública para descobrir OSCs por informações institucionais e territoriais.",
                    "limitation": (
                        "O Mapa reúne dados de bases públicas e informações fornecidas pelas próprias OSCs. "
                        "Não comprova atendimento atual, gratuidade, vagas, foco exclusivo em mulheres ou "
                        "liderança feminina. Coletivos informais podem não constar por não serem OSCs formalizadas."
                    ),
                },
                {
                    "name": "Ministério das Mulheres — Painel da Rede de Atendimento",
                    "url": MINISTRY_PANEL_URL,
                    "scope": "Serviços públicos e especializados da rede de atendimento à mulher.",
                    "limitation": "Não substitui a validação direta de funcionamento e critérios de cada serviço.",
                },
                {
                    "name": "Ligue 180",
                    "url": LIGUE_180_URL,
                    "scope": "Orientação e encaminhamento para serviços da rede de atendimento local.",
                    "limitation": "Não é um cadastro geral de todos os coletivos ou iniciativas comunitárias.",
                },
            ],
            "validation_checklist": [
                "Confirmar que a organização existe e que seu canal de contato está publicado em fonte institucional própria ou governamental.",
                "Confirmar atuação no município/UF e se está aceitando novas pessoas atendidas.",
                "Confirmar gratuitamente quais atividades são oferecidas, critérios, horários e necessidade de encaminhamento.",
                "Confirmar se a iniciativa é criada por mulheres, liderada por mulheres ou especificamente destinada a mulheres; não inferir isso pelo nome.",
                "Verificar a data da última atualização e registrar fonte e data da conferência.",
                "Não divulgar endereço sigiloso de abrigo nem dados pessoais de atendidas.",
            ],
            "automated_organization_results": False,
            "important_notice": (
                "As iniciativas listadas têm informações institucionais sobre público e gratuidade, "
                "mas a presença na lista não confirma vaga, resposta imediata ou atendimento disponível "
                "no município informado. Contate a organização pelos canais oficiais. O cadastro no "
                "Elas Conectadas nunca é exigido para consultar informações."
            ),
            "verification_status": f"official_organization_pages_checked_{VERIFICATION_DATE}",
        }
