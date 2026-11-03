"""Orientação para localizar assistência jurídica gratuita em fontes públicas oficiais."""
from __future__ import annotations

from typing import Any

CNJ_DIRECTORY_URL = "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/"
CONDEGE_DIRECTORY_URL = "https://www.condege.org.br/portal/secretarias"
MINISTRY_GUIDANCE_URL = "https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/agosto-defeso-eleitoral/especial-lei-maria-da-penha-saiba-onde-e-como-buscar-ajuda-em-casos-de-violencia-domestica-e-familiar"
LIGUE_180_URL = "https://www.gov.br/mulheres/pt-br/ligue180"
PANEL_URL = "https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento"


class FreeLegalAidDirectory:
    """Não inventa unidades locais; encaminha a diretórios institucionais verificados."""

    def guide(
        self, *, uf: str | None = None, municipality: str | None = None
    ) -> dict[str, Any]:
        if uf and (len(uf.strip()) != 2 or not uf.strip().isalpha()):
            raise ValueError("Informe a sigla da UF com duas letras.")
        if municipality and len(municipality.strip()) < 2:
            raise ValueError("Informe um município válido.")
        return {
            "service": "Assistência jurídica gratuita",
            "requested_location": {
                "uf": uf.strip().upper() if uf else None,
                "municipality": municipality.strip() if municipality else None,
            },
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
