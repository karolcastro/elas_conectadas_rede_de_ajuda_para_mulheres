"""Fontes de descoberta para ONGs e coletivos com validação reforçada."""
from __future__ import annotations

from typing import Any

IPEA_MAP_URL = "https://mapaosc.ipea.gov.br/"
MINISTRY_PANEL_URL = "https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento"
LIGUE_180_URL = "https://www.gov.br/mulheres/pt-br/ligue180"


class WomenOrganizationsGuide:
    """Oferece fontes de descoberta, sem afirmar que uma OSC atende mulheres ou é gratuita."""

    def guide(
        self, *, uf: str | None = None, municipality: str | None = None
    ) -> dict[str, Any]:
        if uf and (len(uf.strip()) != 2 or not uf.strip().isalpha()):
            raise ValueError("Informe a sigla da UF com duas letras.")
        if municipality and len(municipality.strip()) < 2:
            raise ValueError("Informe um município válido.")
        return {
            "purpose": "Descobrir organizações da sociedade civil, ONGs e iniciativas de apoio a mulheres.",
            "requested_location": {
                "uf": uf.strip().upper() if uf else None,
                "municipality": municipality.strip() if municipality else None,
            },
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
                "Esta ferramenta indica fontes de descoberta e critérios de validação; não retorna "
                "uma lista de ONGs locais já confirmadas. O cadastro no Mapa das OSC não é requisito "
                "para a mulher consultar informações. Não solicite cadastro, login ou dados pessoais."
            ),
            "verification_status": "official_discovery_sources_checked_2026-11-03",
        }
