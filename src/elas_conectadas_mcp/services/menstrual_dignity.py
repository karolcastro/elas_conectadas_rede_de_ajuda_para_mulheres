"""Orientações oficiais sobre o Programa Dignidade Menstrual."""
from __future__ import annotations

from typing import Any

PROGRAM_URL = "https://www.gov.br/pt-br/servicos/obter-autorizacao-para-retirada-gratuita-de-absorventes-higienicos-em-estabelecimentos-do-farmacia-popular"
MINISTRY_FAQ_URL = "https://www.gov.br/saude/pt-br/composicao/saps/dignidade-menstrual/faq"
PHARMACY_LOCATOR_URL = "https://www.gov.br/saude/pt-br/composicao/sectics/farmacia-popular"


class MenstrualDignityGuide:
    """Expõe critérios e etapas com base nas páginas oficiais consultadas."""

    def get_guidance(self) -> dict[str, Any]:
        return {
            "program_name": "Programa Dignidade Menstrual",
            "benefit": "Retirada gratuita de absorventes higiênicos em farmácias credenciadas ao Farmácia Popular.",
            "eligibility_summary": {
                "age_range": "10 a 49 anos",
                "cadunico": "A página oficial do serviço informa inscrição no CadÚnico e enquadramento em pelo menos uma situação prevista: estudante de baixa renda da rede pública, renda mensal por pessoa até o limite oficial vigente ou situação de rua.",
                "income_threshold": "A página do serviço gov.br consultada em 03/11/2026 informa renda mensal de até R$ 218 por pessoa. Se houver divergência em páginas oficiais, confirmar no serviço oficial antes de orientar a elegibilidade individual.",
                "other_criteria": "Estudante de baixa renda da rede pública ou pessoa em situação de rua, conforme critérios oficiais e comprovação aplicável.",
            },
            "benefit_quantity": "Até 40 unidades a cada período de 56 dias.",
            "authorization_validity": "180 dias, conforme orientação oficial do Ministério da Saúde.",
            "how_to_access": [
                "Emitir a autorização pelo Meu SUS Digital, na opção Dignidade Menstrual > Emitir autorização.",
                "Se não conseguir emitir digitalmente, procurar uma UBS para orientação e apoio.",
                "A página oficial também indica apoio de CRAS, CREAS, Centro POP e Consultório na Rua.",
                "Apresentar na farmácia credenciada a autorização (digital ou impressa) e documento oficial com foto e CPF.",
                "Consultar o painel oficial do Farmácia Popular para localizar estabelecimentos credenciados.",
            ],
            "important_access_note": "A consulta de informações no Elas Conectadas não exige cadastro. A emissão da autorização no Meu SUS Digital pode exigir autenticação gov.br, conforme o fluxo oficial do serviço.",
            "official_sources": [PROGRAM_URL, MINISTRY_FAQ_URL, PHARMACY_LOCATOR_URL],
            "checked_at": "2026-11-03",
            "availability_notice": "O guia explica o programa; não confirma estoque de absorventes em uma farmácia específica. Confirme a disponibilidade diretamente com o estabelecimento.",
        }
