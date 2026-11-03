"""Diretório de cursos e oportunidades gratuitos para mulheres, com status transparente."""
from __future__ import annotations

from typing import Any

PROGRAMS = [
    {
        "id": "sp-qualifica-ela-empreende",
        "name": "Ela Empreende! — Qualifica SP",
        "provider": "Governo do Estado de São Paulo / Qualifica SP",
        "audience": "Mulheres que desejam iniciar ou fortalecer pequenos negócios.",
        "coverage": "SP",
        "ufs": ["SP"],
        "format": "Online, pelo WhatsApp",
        "free": True,
        "certificate": True,
        "content": ["planejamento", "organização financeira", "marketing digital", "acesso a crédito"],
        "enrollment_status": "inscrições contínuas até o preenchimento das vagas, conforme informação oficial publicada em 10/09/2026; confirmar disponibilidade no portal antes de orientar a inscrição",
        "application_url": "https://www.qualificasp.sp.gov.br/",
        "official_source": "https://www.desenvolvimentoeconomico.sp.gov.br/DesenvolvimentoEconomico/noticias/qualifica%2Bsp%2Boferece%2Bcursos%2Bgratuitos%2Bpara%2Bquem%2Bquer%2Bempreender%2Bou%2Bmelhorar%2Ba%2Bgestao%2Bdo%2Bnegocio",
        "verification_date": "2026-11-03",
        "requires_external_account": "O portal informa fluxo de inscrição com conta gov.br; o agente nunca deve solicitar credenciais.",
        "status_note": "O site oficial lista o curso e a inscrição; vagas podem se esgotar e devem ser confirmadas no destino.",
    },
    {
        "id": "br-mds-educacao-financeira-mulheres",
        "name": "Educação Financeira para Mulheres Empreendedoras — módulos 1 e 2",
        "provider": "Ministério do Desenvolvimento e Assistência Social — Portal de Educação Empreendedora",
        "audience": "Mulheres empreendedoras.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online",
        "free": True,
        "content": [
            "metas e saúde financeira pessoal e do negócio",
            "registros e custos do negócio",
            "plano de negócios",
            "crédito e gestão de crises",
        ],
        "enrollment_status": "curso listado no portal oficial consultado em 03/11/2026; confirmar acesso e condições na página do curso",
        "application_url": "https://www.gov.br/mds/pt-br/acoes-e-programas/programa-acredita-no-primeiro-passo/quero-empreender/portal-de-educacao-empreendedora",
        "official_source": "https://www.gov.br/mds/pt-br/acoes-e-programas/programa-acredita-no-primeiro-passo/quero-empreender/portal-de-educacao-empreendedora",
        "verification_date": "2026-11-03",
        "status_note": "A página descreve os módulos como gratuitos; não afirma disponibilidade de mentoria ou vaga individual.",
    },
    {
        "id": "br-mec-mulheres-mil",
        "name": "Programa Mulheres Mil — cursos profissionalizantes",
        "provider": "Ministério da Educação / Rede Federal e redes estaduais",
        "audience": "Mulheres maiores de 16 anos em situação de vulnerabilidade social, incluindo vítimas de violência e mulheres com baixa ou nenhuma escolaridade, conforme regras do programa e de cada oferta.",
        "coverage": "Oferta divulgada para novembro e dezembro de 2026",
        "ufs": ["MG", "PE", "PR", "ES", "RN", "BA"],
        "format": "Presencial; oferta definida por instituição e edital local",
        "free": True,
        "enrollment_status": "Agência Gov/MEC informou em 03/11/2026 a previsão de 230 vagas em 11 cursos presenciais para novembro e dezembro, nos estados MG, PE, PR, ES, RN e BA. A existência de oferta não garante inscrição aberta ou vaga remanescente.",
        "application_url": "https://app.powerbi.com/view?r=eyJrIjoiYTRjMTlkNDUtNjBlYy00NjIyLTkxYjQtNGE3MzNmZDc0OWUwIiwidCI6ImI4YzI1OTMyLTVlNzYtNGIyYi05YzUzLWQ0MTc0NWU5YzkyZCJ9",
        "official_source": "https://agenciagov.ebc.com.br/noticias/202611/programa-mulheres-mil-oferece-230-vagas-gratuitas-em-cursos-de-qualificacao-profissional",
        "opportunity_directory_url": "https://app.powerbi.com/view?r=eyJrIjoiYTRjMTlkNDUtNjBlYy00NjIyLTkxYjQtNGE3MzNmZDc0OWUwIiwidCI6ImI4YzI1OTMyLTVlNzYtNGIyYi05YzUzLWQ0MTc0NWU5YzkyZCJ9",
        "verification_date": "2026-11-03",
        "status_note": "No Painel de Oportunidades do Pronatec, filtre Mulheres Mil e selecione Novembro ou Dezembro. Depois, confirme requisitos, prazo e inscrição diretamente com a instituição responsável. Não presumir que vagas continuam abertas.",
    },
]


class WomenTrainingDirectory:
    """Lista oportunidades verificadas sem prometer vagas ou recolher dados pessoais."""

    def search(self, *, uf: str | None = None) -> dict[str, Any]:
        normalized_uf = uf.strip().upper() if uf else None
        if normalized_uf and (len(normalized_uf) != 2 or not normalized_uf.isalpha()):
            raise ValueError("Informe a sigla da UF com duas letras.")
        matches = [
            item for item in PROGRAMS
            if not normalized_uf
            or item["coverage"] == "Brasil"
            or normalized_uf in item.get("ufs", [])
        ]
        return {
            "programs": matches,
            "count": len(matches),
            "filter": {"uf": normalized_uf},
            "important_notice": (
                "Gratuidade e público-alvo são descritos nas fontes indicadas. Vagas, inscrições, "
                "datas, elegibilidade e disponibilidade podem mudar; confirme no portal oficial "
                "ou com a instituição antes de se inscrever. O agente não solicita CPF, senha, "
                "login, e-mail ou documentos. Se um serviço externo exigir conta gov.br, a usuária "
                "deve acessar diretamente o site oficial e nunca compartilhar a senha com o agente."
            ),
        }
