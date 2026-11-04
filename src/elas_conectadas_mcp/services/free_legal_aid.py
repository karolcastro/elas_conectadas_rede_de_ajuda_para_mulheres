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
