"""Referência segura ao Painel oficial da Rede de Atendimento à Mulher."""
from __future__ import annotations

from typing import Any

PANEL_URL = "https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento"
MINISTRY_SOURCE_URL = "https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2024/fevereiro/ministerio-das-mulheres-cria-painel-com-informacoes-sobre-a-rede-de-atendimento-a-mulher"

PANEL_SERVICE_TYPES = [
    "Delegacias Especializadas de Atendimento à Mulher e núcleos/postos em delegacias gerais",
    "Núcleos da Mulher nas Defensorias Públicas (NUDEM)",
    "Promotorias especializadas e núcleos de gênero nos Ministérios Públicos",
    "Juizados e Varas especializadas em violência doméstica e familiar",
    "Centros de Referência e de Atendimento à Mulher (CRAM/CEAM)",
    "Casas Abrigo, acolhimento provisório e casas de passagem",
    "Serviços de saúde para pessoas em situação de violência sexual",
    "Casa da Mulher Brasileira",
    "Patrulhas Maria da Penha",
]

class OfficialNetworkDirectory:
    """Não faz scraping nem simula busca; encaminha ao painel oficial consultável."""

    def guide(self, *, uf: str | None = None, municipality: str | None = None, category: str | None = None) -> dict[str, Any]:
        if uf and (len(uf.strip()) != 2 or not uf.strip().isalpha()):
            raise ValueError("Informe a sigla da UF com duas letras.")
        if municipality and len(municipality.strip()) < 2:
            raise ValueError("Informe um município válido.")
        if category and category not in PANEL_SERVICE_TYPES:
            raise ValueError("Tipo de serviço não reconhecido no catálogo do painel.")
        return {
            "official_panel_url": PANEL_URL,
            "ministry_explainer_url": MINISTRY_SOURCE_URL,
            "search_filters_requested": {
                "uf": uf.strip().upper() if uf else None,
                "municipality": municipality.strip() if municipality else None,
                "service_type": category,
            },
            "known_service_types": PANEL_SERVICE_TYPES,
            "instructions": [
                "Abra o Painel da Rede de Atendimento do Ministério das Mulheres.",
                "Na seção de serviços da rede, selecione região/estado e município.",
                "Confira o tipo de serviço, endereço público e contato exibidos pelo próprio painel.",
                "Antes de se deslocar, confirme funcionamento e forma de atendimento diretamente com o serviço.",
                "Para casas-abrigo, não divulgue nem solicite endereço sigiloso; peça orientação segura pelo Ligue 180.",
            ],
            "integration_status": "official_link_and_guidance_only",
            "automated_records_available": False,
            "important_notice": "O painel é oficial e permite pesquisa por região, estado e município. Não foi identificada nesta implementação uma API pública documentada para consultar seus registros automaticamente; por isso, esta ferramenta não afirma ter localizado unidades nem reproduz dados do painel.",
            "verification_date": "2026-11-03",
        }
