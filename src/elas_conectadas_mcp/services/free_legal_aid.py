"""Orientação para localizar assistência jurídica gratuita em fontes públicas oficiais."""
from __future__ import annotations

from typing import Any

CNJ_DIRECTORY_URL = "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/"
CONDEGE_DIRECTORY_URL = "https://www.condege.org.br/portal/secretarias"
MINISTRY_GUIDANCE_URL = "https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/agosto-defeso-eleitoral/especial-lei-maria-da-penha-saiba-onde-e-como-buscar-ajuda-em-casos-de-violencia-domestica-e-familiar"
LIGUE_180_URL = "https://www.gov.br/mulheres/pt-br/ligue180"
PANEL_URL = "https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento"
SP_DEFENSORIA_SERVICE_URL = "https://servicos.sp.gov.br/fcarta/2C493B4D-3542-4441-9DD4-60E7285C8DAB"
SP_DEFENSORIA_ADDRESSES_URL = "https://www.defensoria.sp.def.br/institucional/enderecos-e-telefones"
SP_WOMEN_RIGHTS_URL = "https://www.defensoria.sp.def.br/nucleos-especializados/pagina-inicial-nucleos-especializados/direitos-das-mulheres/redes-de-atendimento/violencia-domestica-e-familiar"
BA_DEFENSORIA_SERVICE_URL = "https://www.ba.gov.br/servico/dpe/solicitar-atendimento-na-defensoria-publica-do-estado-ba"
BA_DEFENSORIA_CONTACT_URL = "https://www.ba.gov.br/ouvidoria/120/dpe"
PR_DEFENSORIA_SERVICE_URL = "https://www.parana.pr.gov.br/servicos/Servicos/Mulher/Solicitar-atendimento-na-Defensoria-Publica-do-Estado-do-Parana-K03Yaq34"
PR_NUDEM_URL = "https://www.defensoriapublica.pr.def.br/Pagina/Nucleo-de-Promocao-e-Defesa-dos-Direitos-das-Mulheres"
MG_NUDEM_URL = "https://defensoria.mg.def.br/contatos-para-o-atendimento/"
PE_NUDEM_URL = "https://www.defensoria.pe.def.br/noticias/detalhe/4300/"
PE_CAPITAL_DIRECTORY_URL = "https://www.defensoria.pe.def.br/enderecos/capital/"
CREAS_MDS_URL = "https://www.gov.br/mds/pt-br/acoes-e-programas/SUAS/unidades-de-atendimento/centro-de-referencia-especializado-de-assistencia-social-creas"


class FreeLegalAidDirectory:
    """Não inventa unidades locais; encaminha a diretórios institucionais verificados."""

    def guide(
        self, *, uf: str | None = None, municipality: str | None = None
    ) -> dict[str, Any]:
        if uf and (len(uf.strip()) != 2 or not uf.strip().isalpha()):
            raise ValueError("Informe a sigla da UF com duas letras.")
        if municipality and len(municipality.strip()) < 2:
            raise ValueError("Informe um município válido.")
        normalized_uf = uf.strip().upper() if uf else None
        state_specific_contacts = []
        if normalized_uf == "SP":
            state_specific_contacts.append({
                "name": "Defensoria Pública do Estado de São Paulo — agendamento e informações",
                "phone": "0800 773 4340",
                "service_hours": "Segunda a sexta, das 7h às 19h (dias úteis). Fins de semana e feriados: das 7h às 12h, casos urgentes exclusivamente pelo site com a assistente virtual Júlia.",
                "free": True,
                "audience": "Pessoas que não têm condições financeiras de pagar por advogado; a triagem e os critérios aplicáveis devem ser confirmados diretamente.",
                "appointment_required": True,
                "documents_required_to_request": False,
                "online_access": "https://www.defensoria.sp.def.br/atendimento/agende-seu-atendimento",
                "official_source": SP_DEFENSORIA_SERVICE_URL,
                "source_last_updated": "2026-09-09",
                "important_notice": "A página estadual informa que o pedido inicial de atendimento pode ser solicitado sem apresentar documentos. Isso não significa que documentos nunca serão necessários em etapas posteriores."
            })
            state_specific_contacts.append({
                "name": "Núcleo Especializado de Promoção e Defesa dos Direitos das Mulheres — NUDEM/SP",
                "phone": None,
                "email": None,
                "official_source": SP_WOMEN_RIGHTS_URL,
                "source_last_updated": "2024-06",
                "purpose": "Página institucional com orientações sobre direitos e rede de atendimento para mulheres em situação de violência. Não há telefone direto atual confirmado nesta fonte; utilize o canal geral da Defensoria para confirmar encaminhamento ao núcleo."
            })
        if normalized_uf == "BA":
            state_specific_contacts.append({
                "name": "Defensoria Pública do Estado da Bahia — Disque Defensoria",
                "phone": "129 ou 0800 071 3121",
                "service_hours": "Segunda a sexta-feira, das 8h às 17h.",
                "free": True,
                "audience": "Pessoas sem condições financeiras de arcar com assistência jurídica ou em situação de vulnerabilidade social; confirme a triagem diretamente.",
                "appointment_required": None,
                "online_access": BA_DEFENSORIA_SERVICE_URL,
                "official_source": BA_DEFENSORIA_CONTACT_URL,
                "source_last_updated": "2026-07-17",
                "important_notice": "A página oficial consultada apresenta os telefones como Disque Defensoria e informa ligação gratuita. O horário e a opção de atendimento devem ser confirmados diretamente; a página de serviço estadual explica como solicitar assistência jurídica gratuita."
            })
        if normalized_uf == "PR":
            state_specific_contacts.append({
                "name": "Defensoria Pública do Estado do Paraná — informações e atendimento",
                "phone": "(41) 99123-1961",
                "free": True,
                "audience": "Em geral, pessoas com renda familiar de até três salários mínimos; a página estadual cita exceções, inclusive mulheres vítimas de violência doméstica e familiar, independentemente de renda.",
                "appointment_required": False,
                "online_access": "https://agendamento.defensoria.pr.def.br/",
                "official_source": PR_DEFENSORIA_SERVICE_URL,
                "source_last_updated": "2026-11-03",
                "important_notice": "A página estadual informa atendimento presencial gratuito, com agendamento online recomendado, mas também possibilidade de comparecer diretamente a uma sede. Documentos são solicitados na triagem inicial; confirme a unidade e a lista atualizada antes de se deslocar."
            })
            state_specific_contacts.append({
                "name": "Núcleo de Promoção e Defesa dos Direitos das Mulheres — NUDEM/PR",
                "phone": "(41) 99285-8134",
                "email": "nudem@defensoria.pr.def.br",
                "service_hours": "Segunda a sexta-feira, das 10h às 17h.",
                "free": True,
                "appointment_required": True,
                "service_modes": ["presencial", "remoto"],
                "official_source": PR_NUDEM_URL,
                "source_last_updated": "2026-09-29",
                "purpose": "Núcleo especializado em promoção e defesa dos direitos das mulheres; atendimento somente com agendamento."
            })
        if normalized_uf == "MG":
            state_specific_contacts.append({
                "name": "Defensoria Pública de Minas Gerais — NUDEM/Belo Horizonte",
                "phone": "(31) 98475-2616 / (31) 98239-8863",
                "service_hours": "Segunda a sexta-feira, das 11h às 17h.",
                "free": True,
                "service_modes": ["chamada", "WhatsApp"],
                "email": "atendimentonudembh@defensoria.mg.def.br",
                "official_source": MG_NUDEM_URL,
                "source_last_updated": "2025-06-23",
                "important_notice": "Contato publicado para o NUDEM em Belo Horizonte. Não presumir que seja canal de atendimento de todo o estado; para outras cidades, consulte a lista de unidades e contatos psicossociais no site oficial."
            })
        if normalized_uf == "PE":
            state_specific_contacts.append({
                "name": "Defensoria Pública de Pernambuco — NUDEM",
                "phone": "(81) 99488-3765",
                "service_hours": "Página de endereços informa 8h às 16h; confirme disponibilidade por mensagem.",
                "free": True,
                "service_modes": ["WhatsApp por mensagem"],
                "email": "defesadamulher@defensoria.pe.gov.br",
                "appointment_required": False,
                "official_source": PE_NUDEM_URL,
                "source_last_updated": "2026-09-25",
                "important_notice": "A notícia oficial informa que o atendimento inicial é exclusivamente por mensagem e respondido por ordem de chegada. Se for necessário comparecer à sede após orientação, a notícia informa que não é necessário agendamento prévio. O endereço/horário devem ser confirmados na página oficial da capital."
            })
        return {
            "service": "Assistência jurídica gratuita",
            "requested_location": {
                "uf": normalized_uf,
                "municipality": municipality.strip() if municipality else None,
            },
            "state_specific_contacts": state_specific_contacts,
            "official_directories": [
                {
                    "name": "Conselho Nacional de Justiça — Defensorias Públicas",
                    "url": CNJ_DIRECTORY_URL,
                    "purpose": "Lista as Defensorias Públicas estaduais e seus canais institucionais.",
                },
                {
                    "name": "CONDEGE — Defensorias Públicas",
                    "url": CONDEGE_DIRECTORY_URL,
                    "purpose": "Diretório institucional complementar das Defensorias Públicas.",
                },
                {
                    "name": "Ministério das Mulheres — orientação sobre a rede de atendimento",
                    "url": MINISTRY_GUIDANCE_URL,
                    "purpose": "Explica o papel da Defensoria e outros serviços para mulheres em situação de violência.",
                },
                {
                    "name": "Ligue 180",
                    "url": LIGUE_180_URL,
                    "purpose": "Orienta sobre direitos e indica serviços da rede local; atendimento gratuito 24 horas.",
                },
                {
                    "name": "Ministério do Desenvolvimento e Assistência Social — CREAS",
                    "url": CREAS_MDS_URL,
                    "purpose": "Serviço público e gratuito de proteção social especial para pessoas e famílias com direitos violados, incluindo violência física, psicológica e sexual; permite localizar unidades por município.",
                    "source_last_updated": "2026-10-26",
                },
                {
                    "name": "Painel da Rede de Atendimento",
                    "url": PANEL_URL,
                    "purpose": "Permite localizar serviços da rede por estado e município.",
                },
            ],
            "how_to_access": [
                "Abra o diretório do CNJ e selecione a Defensoria Pública do estado informado.",
                "No site oficial da Defensoria, procure atendimento à mulher, violência doméstica ou NUDEM.",
                "Confirme diretamente critérios de atendimento, documentos, agendamento, modalidade e gratuidade.",
                "Em São Paulo, use o telefone estadual 0800 773 4340 ou o agendamento online; o atendimento exige agendamento prévio.",
                "Na Bahia, use o Disque Defensoria 129 ou 0800 071 3121; confirme a opção adequada e os critérios diretamente com a DPE-BA.",
                "No Paraná, consulte o NUDEM pelo telefone (41) 99285-8134 ou e-mail nudem@defensoria.pr.def.br; o núcleo atende somente com agendamento, presencial ou remotamente.",
                "Em Minas Gerais, os contatos publicados do NUDEM em Belo Horizonte são (31) 98475-2616 e (31) 98239-8863, de 11h às 17h; para outras cidades, consulte a lista oficial de unidades.",
                "Em Pernambuco, o NUDEM recebe mensagens pelo WhatsApp (81) 99488-3765; atendimento inicial exclusivamente por mensagem e resposta por ordem de chegada.",
                "Para apoio socioassistencial gratuito em qualquer estado, procure o CREAS municipal; consulte a unidade no localizador oficial do MDS. Se não houver CREAS no município, procure a assistência social da prefeitura.",
                "Para demanda relacionada à violência contra a mulher em São Paulo, consulte a página do NUDEM; se não houver contato direto publicado, solicite encaminhamento pelo canal geral da Defensoria.",
                "Se não encontrar o núcleo local, use o Ligue 180 para orientação e encaminhamento na rede.",
            ],
            "important_rights": (
                "A Defensoria Pública presta orientação e assistência jurídica gratuita nos termos "
                "das regras institucionais. Critérios de triagem e fluxos variam por estado e caso; "
                "não presuma que a usuária está inelegível sem confirmação do órgão. O Ministério "
                "das Mulheres orienta que mulheres em situação de violência podem buscar a Defensoria "
                "para orientação e proteção jurídica."
            ),
            "automated_local_results": False,
            "verification_status": "official_directory_links_verified_2026-11-03",
            "important_notice": (
                "Esta ferramenta não afirma ter localizado uma unidade municipal nem confirma "
                "horários ou vagas. Não envie CPF, documentos, relatos de violência ou dados "
                "sensíveis ao agente para obter estes links."
            ),
        }
