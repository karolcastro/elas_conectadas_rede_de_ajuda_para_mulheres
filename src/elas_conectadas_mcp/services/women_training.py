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
    {
        "id": "br-womakerscode-introducao-ia",
        "name": "Introdução à Inteligência Artificial — Mais Mulheres em Tech",
        "provider": "WoMakersCode / Mais Mulheres em Tech",
        "audience": "Mulheres interessadas em aprender fundamentos de IA generativa e aplicações práticas no trabalho, nos estudos e no cotidiano.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online, autoinstrucional",
        "free": True,
        "certificate": True,
        "priority": 0,
        "women_specific": True,
        "opportunity_type": "curso",
        "content": ["fundamentos de inteligência artificial", "IA generativa", "produtividade", "uso responsável de IA", "Copilot e ferramentas digitais"],
        "enrollment_status": "Página oficial do curso acessível na verificação de 04/11/2026. A página não informa prazo de inscrição nem quantidade de vagas; confirme se o acesso continua disponível na plataforma.",
        "application_url": "https://www.maismulheres.tech/courses/introducao-inteligencia-artificial",
        "official_source": "https://www.womakerscode.org/programas",
        "verification_date": "2026-11-04",
        "status_note": "A página do curso declara modalidade online, gratuidade e certificado. A plataforma Mais Mulheres em Tech é apresentada como criada por mulheres para mulheres. A disponibilidade de acesso deve ser reconfirmada no destino.",
    },
    {
        "id": "br-womakerscode-como-conseguir-emprego",
        "name": "Como Conseguir um Emprego — Mais Mulheres em Tech",
        "provider": "WoMakersCode / Mais Mulheres em Tech",
        "audience": "Mulheres que buscam o primeiro emprego ou recolocação profissional.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online, autoinstrucional",
        "free": True,
        "certificate": True,
        "priority": 0,
        "women_specific": True,
        "opportunity_type": "curso",
        "content": ["currículo", "busca de vagas", "candidaturas", "LinkedIn", "preparação para entrevistas"],
        "enrollment_status": "Página oficial do curso acessível na verificação de 04/11/2026. A página não informa prazo de inscrição nem quantidade de vagas; confirme se o acesso continua disponível na plataforma.",
        "application_url": "https://www.maismulheres.tech/courses/como-conseguir-um-emprego",
        "official_source": "https://www.womakerscode.org/programas",
        "verification_date": "2026-11-04",
        "status_note": "A página do curso declara modalidade online, gratuidade e certificado. A plataforma Mais Mulheres em Tech é apresentada como criada por mulheres para mulheres. A disponibilidade de acesso deve ser reconfirmada no destino.",
    },
    {
        "id": "br-womakerscode-lideranca-feminina",
        "name": "Liderança Feminina e Soft Skills — Mais Mulheres em Tech",
        "provider": "WoMakersCode / Mais Mulheres em Tech",
        "audience": "Mulheres interessadas em desenvolver liderança, comunicação e habilidades profissionais.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online, conteúdo gravado e autoinstrucional",
        "free": True,
        "certificate": True,
        "priority": 0,
        "women_specific": True,
        "opportunity_type": "curso",
        "content": ["liderança feminina", "soft skills", "autoconhecimento", "planejamento de carreira", "comunicação", "organização financeira"],
        "enrollment_status": "Conteúdo gravado disponível na página oficial consultada em 04/11/2026. Não é uma turma ao vivo; confirme acesso e condições de certificado na plataforma.",
        "application_url": "https://www.maismulheres.tech/courses/lideranca-feminina-e-soft-skills",
        "official_source": "https://www.womakerscode.org/programas",
        "verification_date": "2026-11-04",
        "status_note": "A página declara que o conteúdo é gratuito, online, com interpretação em Libras e certificado. O curso reúne gravações de um bootcamp realizado em 2020; não deve ser apresentado como turma nova ou mentoria ao vivo.",
    },,
    {
        "id": "br-programaria-sprint-processos-seletivos-tech",
        "name": "PrograMaria Sprint — Processos Seletivos em Tech",
        "provider": "PrograMaria",
        "audience": "Principalmente mulheres cis e trans e pessoas de gêneros minorizados que atuam ou têm interesse em tecnologia; sem limite de idade informado.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online, autoinstrucional, com artigos, vídeos e atividades; acesso ao conteúdo por seis semanas após a inscrição.",
        "free": True,
        "certificate": True,
        "priority": 0,
        "women_specific": True,
        "opportunity_type": "sprint",
        "content": ["preparação de currículo, LinkedIn e GitHub", "busca e avaliação de vagas", "pretensão salarial e networking", "entrevistas com RH e técnicas", "testes técnicos", "negociação de propostas e desenvolvimento de carreira"],
        "enrollment_status": "A página oficial informa inscrições por tempo indeterminado e participação gratuita. Acesso e condições devem ser confirmados no portal no momento da consulta.",
        "application_url": "https://vamosjuntes.programaria.org/sprint-processos-seletivos",
        "official_source": "https://vamosjuntes.programaria.org/sprint-processos-seletivos",
        "verification_date": "2026-11-04",
        "status_note": "A página descreve quatro módulos, material online, certificado digital e acesso durante seis semanas após a inscrição. Não exige experiência prévia; recomenda computador para melhor aproveitamento."
    },
    {
        "id": "br-programaria-sprint-ia-generativa",
        "name": "PrograMaria Sprint — IA Generativa",
        "provider": "PrograMaria",
        "audience": "Principalmente mulheres cis e trans, pessoas não-binárias e outros gêneros minorizados que atuam ou têm interesse em dados, tecnologia e IA generativa.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online, minicurso com nove módulos, atividades, lives, vídeos, artigos e interação.",
        "free": True,
        "priority": 0,
        "women_specific": True,
        "opportunity_type": "minicurso",
        "content": ["fundamentos de IA generativa e LLMs", "prompts e uso responsável", "vieses algorítmicos", "GitHub Copilot", "APIs OpenAI e Gemini", "tools e agentes inteligentes", "interfaces inteligentes", "protótipos e buscadores com IA"],
        "enrollment_status": "A página oficial informa inscrições abertas e ilimitadas e participação gratuita na verificação de 04/11/2026. Confirme o acesso no portal antes de orientar a inscrição.",
        "application_url": "https://vamosjuntes.programaria.org/programaria-sprint-ia-generativa",
        "official_source": "https://vamosjuntes.programaria.org/programaria-sprint-ia-generativa",
        "verification_date": "2026-11-04",
        "status_note": "A página não informa certificado nem prazo final. A inscrição encaminha à plataforma externa da PrograMaria; o agente não solicita e-mail, senha ou credenciais."
    },
    {
        "id": "br-programaria-bolsas-formacao-tech-lista-interesse",
        "name": "PrograMaria — Lista de interesse para bolsas em formação tech",
        "provider": "PrograMaria",
        "audience": "Pessoas afetadas por desigualdades de gênero, raça, sexualidade, deficiência, idade e condição socioeconômica; iniciativa inclui mulheres, mas não é exclusiva para elas.",
        "coverage": "Brasil",
        "ufs": [],
        "format": "Online; lista de interesse para futuras seleções de bolsas.",
        "free": True,
        "priority": 0,
        "women_specific": True,
        "opportunity_type": "bolsa_futura_lista_de_interesse",
        "content": ["front-end: HTML, CSS, JavaScript e lógica de programação", "análise de dados: planilhas, Python, Pandas, NumPy, SQL, visualização e fundamentos de machine learning", "back-end: JavaScript, Node.js, APIs, bancos de dados, Git e GitHub"],
        "enrollment_status": "A página oficial exibe listas de interesse, mas informa que as datas dos processos de bolsas serão divulgadas em breve. Não equivale a turma com inscrições abertas nem garante bolsa.",
        "application_url": "https://vamosjuntes.programaria.org/oportunidades-gratuitas",
        "official_source": "https://vamosjuntes.programaria.org/oportunidades-gratuitas",
        "verification_date": "2026-11-04",
        "status_note": "O portal informa que oferece bolsas para pessoas que não conseguem arcar com os cursos e apresenta trilhas de front-end, dados e back-end. A seleção, quantidade de bolsas, datas e critérios de cada edição precisam ser confirmados quando publicados."
    }
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
        matches.sort(key=lambda item: (item.get("priority", 1), item["name"].casefold()))
        return {
            "programs": matches,
            "count": len(matches),
            "filter": {"uf": normalized_uf},
            "important_notice": (
                "Gratuidade e público-alvo são descritos nas fontes indicadas. Vagas, inscrições, "
                "datas, elegibilidade e disponibilidade podem mudar; confirme no portal oficial "
                "ou com a instituição antes de se inscrever. Iniciativas criadas por mulheres "
                "para mulheres ou destinadas especificamente ao público feminino aparecem primeiro. "
                "Comunidades, cursos autoinstrucionais, turmas com inscrições abertas e programas "
                "encerrados devem ser diferenciados. O agente não solicita CPF, senha, login, e-mail "
                "ou documentos. Se um serviço externo exigir conta gov.br, a usuária "
                "deve acessar diretamente o site oficial e nunca compartilhar a senha com o agente."
            ),
        }
