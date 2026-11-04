# Elas Conectadas — Rede de Ajuda para Mulheres

Agente de Inteligência Artificial em desenvolvimento para conectar mulheres a serviços gratuitos de proteção, acolhimento, assistência, orientação e capacitação profissional em todo o Brasil.

## Objetivo

Ajudar mulheres a encontrar serviços confiáveis de acordo com sua necessidade e localização, apresentando contatos, fontes e orientações práticas para acessar o atendimento — **sem exigir cadastro, login, e-mail ou senha**.

## Funcionalidades previstas

- Busca por tipo de ajuda em linguagem natural.
- Busca por CEP (resolução de município via ViaCEP, serviço público de terceiros) ou município/estado.
- Uso opcional da localização atual do dispositivo, somente com autorização explícita.
- Localização de serviços gratuitos de proteção, acolhimento, assistência jurídica, apoio psicológico, social e de saúde da mulher.
- Busca de UBS, ambulatórios e serviços públicos para consultas e exames, distinguindo unidades localizadas de exames efetivamente confirmados.
- Integração implementada no servidor MCP para resolver município/UF via IBGE e consultar estabelecimentos ativos no CNES/DEMAS.
- Pipeline de ingestão, normalização, validação e atualização com fonte e data de verificação.
- Divulgação de campanhas oficiais e iniciativas de ONGs para mulheres e meninas, incluindo dignidade menstrual e acesso a absorventes.
- Busca de cursos, bolsas e capacitações, priorizando iniciativas criadas por mulheres para mulheres ou destinadas especificamente ao público feminino.
- Apresentação de contatos, critérios de atendimento, gratuidade, fonte oficial e data de verificação.
- Orientação sobre como acessar o serviço.
- Informações de segurança digital quando houver risco de monitoramento.

## Segurança e acolhimento

- **Perigo imediato: ligue 190.**
- **Orientação e atendimento sobre violência contra a mulher: Ligue 180.**

O agente deve evitar coleta e armazenamento desnecessários de dados pessoais, não divulgar endereços sigilosos de abrigos e não substituir profissionais ou serviços de emergência.

## Estratégia de informação

O projeto prevê combinar consultas online a fontes oficiais durante cada pesquisa com uma base de dados estruturada e atualizada periodicamente. Informações não confirmadas devem ser identificadas como não verificadas — nunca inventadas ou apresentadas como atuais.

## Padrão de integração

Os agentes e integrações serão estruturados com **MCP (Model Context Protocol)**, expondo ferramentas, recursos e prompts de forma modular e segura. A arquitetura MCP está especificada na documentação; os servidores e tools serão considerados implementados somente após desenvolvimento e testes.

## Tecnologias propostas

| Tecnologia | Uso previsto |
|---|---|
| Python | Lógica do agente e integrações |
| LLM / API de IA | Interpretação de solicitações |
| RAG | Recuperação de informações confiáveis |
| APIs de mapas/geolocalização | Busca por proximidade |
| Supabase | Base de dados |
| n8n ou Make | Atualização automatizada |
| Streamlit | Interface inicial |

Essas tecnologias compõem a arquitetura proposta; a presença nesta lista não significa que todas já estejam implementadas.

## Escopo inicial (MVP)

1. Delegacias da Mulher e canais oficiais de proteção.
2. ONGs e projetos de apoio.
3. Casas de acolhimento, preservando endereços sigilosos.
4. Assistência jurídica gratuita.
5. Centros de atendimento psicológico e social.
6. Cursos gratuitos, bolsas e capacitação para mulheres.
7. Saúde da Mulher: localização de serviços e exames, saúde menstrual e campanhas para mulheres e meninas.

## Documentação

Consulte [docs/AGENTE_ELAS_CONECTADAS.md](docs/AGENTE_ELAS_CONECTADAS.md) para requisitos funcionais, fluxo de atendimento, regras de segurança, critérios de validação, estratégia de atualização e arquitetura proposta.

## Status

Projeto em desenvolvimento com servidor MCP e catálogo de **322 referências**, distribuídas pelas **27 UFs** e por **226 combinações município/UF** (verificação em 04/11/2026). Os 322 IDs são únicos. Há **49 registros com gratuidade expressamente confirmada** e **273 com custo não confirmado**; estes últimos não podem ser apresentados como gratuitos. A cobertura municipal é parcial e não representa todos os municípios. A busca não calcula distância nem confirma disponibilidade operacional. Para cursos, o diretório prioriza iniciativas criadas por mulheres para mulheres, como WoMakersCode / Mais Mulheres em Tech, e diferencia conteúdo autoinstrucional de turmas com inscrições abertas. Consulte a documentação para fontes e limites.


## Código-fonte inicial

O repositório agora contém a primeira implementação Python do servidor MCP:

- `src/elas_conectadas_mcp/server.py`: servidor MCP com Tools, Resource e Prompt.
- `src/elas_conectadas_mcp/connectors/ibge.py`: conector assíncrono para a API oficial de Localidades do IBGE.
- `src/elas_conectadas_mcp/connectors/demas.py`: conector para estabelecimentos e UBS do CNES via API DEMAS.
- `tests/test_ibge_connector.py`: testes automatizados com respostas HTTP simuladas.
- `pyproject.toml`: dependências e configuração do projeto.
- `.env.example`: exemplo sem credenciais.

### Executar localmente

Requisitos: Python 3.11 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Iniciar o servidor MCP:

```bash
elas-conectadas-mcp
```

O servidor usa transporte **stdio**, adequado para integração com um cliente MCP local. Para conectá-lo a um cliente MCP, configure o comando de execução no cliente. Não publique o servidor local em uma URL pública sem implementar autenticação, autorização e controles de segurança apropriados.

### Tools disponíveis nesta primeira versão

- `listar_estados`
- `listar_municipios(uf)`
- `consultar_municipio(codigo_ibge)`
- `buscar_estabelecimentos_saude(codigo_municipio, codigo_uf, codigo_tipo_unidade, status, limite, pagina)`
- `consultar_estabelecimento_cnes(codigo_cnes)`
- `listar_ubs_cnes(limite, pagina)`

Resources disponíveis: `ibge://estados` e `demas://fontes`.

Prompt disponível: `orientar_busca_por_municipio`.

**Limite desta versão:** o conector IBGE padroniza referências territoriais. Ele consulta registros de estabelecimentos e UBS no CNES por meio da API DEMAS. Ainda não confirma oferta de exames, agenda, gratuidade ou disponibilidade operacional; também não consulta campanhas nem ONGs. Essas integrações serão implementadas nas próximas etapas. Os testes estão no repositório, mas ainda precisam ser executados em ambiente Python para confirmar o funcionamento.


## Busca municipal de unidades de saúde (MCP)

A ferramenta `buscar_unidades_saude_por_municipio` recebe município e UF, resolve o código territorial pela API do IBGE e consulta estabelecimentos ativos no CNES/DEMAS. A resposta preserva os códigos usados e inclui fonte e ressalvas. O cadastro não confirma agenda, atendimento atual, gratuidade ou realização de exame específico.

Para instalar e testar: `pip install -e ".[dev]"` e `pytest`. Os testes ainda precisam ser executados no ambiente Python antes de considerar a integração validada.


### Busca por CEP — limite importante

O conector ViaCEP consulta um serviço público de terceiros, sem autenticação, para obter município, UF e código IBGE associados ao CEP. A busca seguinte localiza registros CNES no município; ela não determina a unidade mais próxima do endereço nem confirma a realização de exames, gratuidade, agenda ou funcionamento atual. O usuário também pode informar diretamente município e UF, sem fornecer CEP.


## Módulo inicial de proteção

O catálogo `data/servicos_protecao.json` contém somente canais nacionais oficiais já cadastrados: 190 (emergência policial) e 180 (Central de Atendimento à Mulher). O servidor MCP expõe `consultar_telefones_de_urgencia` e `listar_canais_oficiais_de_ajuda`. A busca por delegacias, ONGs, assistência jurídica e acolhimento local depende de registros regionais verificados antes de serem adicionados ao catálogo; nenhum resultado local é inventado ou presumido. Endereços sigilosos de abrigos não devem ser armazenados ou divulgados.

A suíte de testes é executada automaticamente no GitHub Actions. O status atual da validação deve ser conferido na aba Actions; não considere o módulo validado até que testes e lint terminem com sucesso.


O registro do Ligue 180 inclui telefone, WhatsApp (+55 61 9610-0180), e-mail oficial, funcionamento 24 horas e link para o Painel da Rede de Atendimento do Ministério das Mulheres. A ferramenta apresenta o painel oficial como caminho para localizar serviços por estado e município; não afirma ter importado automaticamente os dados do painel.


## Consulta ao Painel oficial da Rede de Atendimento

Foi adicionada a ferramenta MCP `orientar_consulta_rede_oficial_atendimento`, o resource `protecao://painel-rede-atendimento` e o prompt `orientar_acesso_rede_atendimento`. Eles direcionam a usuária ao [Painel da Rede de Atendimento do Ministério das Mulheres](https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento) e explicam como filtrar estado, município e tipo de serviço.

**Limite técnico explícito:** o Ministério documenta que o painel permite consulta por região, estado e cidade e apresenta localização e contatos, mas não foi identificada nesta implementação uma API pública documentada para importar os registros. Portanto, o agente ainda não retorna automaticamente a lista de unidades do painel. A ferramenta fornece encaminhamento ao canal oficial e não simula resultados. A consulta automática só será ativada após identificar uma interface de dados oficialmente suportada e testá-la.


## Saúde menstrual — Programa Dignidade Menstrual

A ferramenta MCP `consultar_programa_dignidade_menstrual`, o resource `saude://dignidade-menstrual` e o prompt `orientar_acesso_absorventes_gratuitos` apresentam critérios, etapas e fontes oficiais do Programa Dignidade Menstrual. A informação é pública e pode ser consultada sem cadastro no Elas Conectadas. A emissão de autorização no serviço externo Meu SUS Digital pode exigir autenticação gov.br; o agente nunca deve solicitar credenciais. O guia não confirma estoque em farmácia específica.


## Segurança e privacidade — controles adicionados

- O .gitignore cobre variantes de .env, chaves privadas, certificados, diretórios de segredos e bancos locais; .env.example permanece versionável.
- Dependências centrais e ferramentas de teste estão fixadas em versões explícitas no pyproject.toml para reduzir variação de instalação.
- O GitHub Actions executa testes, Ruff, Bandit, pip-audit e Gitleaks (incluindo histórico disponível no checkout).
- A busca por CEP transmite o CEP ao ViaCEP, mas a resposta do conector agora retorna somente município, UF e código IBGE; não devolve CEP, rua ou bairro e não persiste esses dados.
- Resource MCP seguranca://privacidade-e-dados e prompt orientar_privacidade_e_seguranca definem minimização, consentimento e proteção de endereços sigilosos.

**Limite importante:** esses controles reduzem riscos, mas não certificam segurança total. Segredos removidos de arquivos atuais ainda podem permanecer no histórico Git; o scanner Gitleaks foi adicionado ao CI para verificar commits disponíveis e precisa concluir com sucesso. A versão atual roda via MCP stdio e não implementa banco ou armazenamento de conversas.


## Assistência jurídica gratuita — diretórios oficiais

Foram adicionados a ferramenta MCP `orientar_assistencia_juridica_gratuita`, o resource `juridico://assistencia-gratuita` e o prompt `orientar_busca_defensoria_mulher`. Eles encaminham a usuária aos diretórios do Conselho Nacional de Justiça e do CONDEGE, além do Ligue 180 e do Painel da Rede de Atendimento.

O agente não simula uma busca municipal: a ferramenta retorna links oficiais e instruções para localizar a Defensoria do estado, procurar atendimento à mulher/NUDEM e confirmar critérios diretamente com a instituição. Para São Paulo, inclui o canal geral 0800 773 4340, horários publicados, gratuidade, agendamento prévio e link institucional do NUDEM. A página estadual informa que não é necessário apresentar documentos para solicitar o serviço, mas documentos podem ser necessários em etapas posteriores. O telefone direto do NUDEM não é exibido porque não foi confirmado em fonte atualizada nesta verificação. Não solicita CPF, documentos ou relato de violência.


## ONGs, coletivos e iniciativas femininas — fontes de descoberta

Foi adicionada a ferramenta MCP orientar_busca_ongs_coletivos_mulheres, o resource comunidade://ongs-e-coletivos e o prompt orientar_validacao_ong_feminina. O módulo aponta o Mapa das OSC do IPEA, o Painel da Rede de Atendimento e o Ligue 180 como fontes para descobrir iniciativas.

**Importante:** o Mapa das OSC é fonte de descoberta, não prova que a organização atende mulheres, é gratuita, está ativa ou é liderada por mulheres. Coletivos informais podem não aparecer. O agente deve validar cada item em fonte institucional antes de recomendar e não simula resultados locais automáticos.


Consulte `SECURITY.md` para a política de divulgação responsável de vulnerabilidades. O Dependabot está configurado para propor atualizações semanais de dependências Python e GitHub Actions.


## Catálogo regional validado — São Paulo (capital)

Foi adicionada a primeira carga regional ao arquivo `data/servicos_protecao.json`, com Delegacias de Defesa da Mulher (DDMs), Casas da Mulher, Centros de Defesa e de Convivência da Mulher (CDCMs) e Casa da Mulher Brasileira da capital paulista. Os registros incluem endereço público divulgado pela Prefeitura, telefone, horário informado, zona, fonte oficial e data de verificação (03/11/2026).

A ferramenta MCP `buscar_servicos_protecao_por_localidade(uf, municipio, categoria)` consulta esse catálogo. O resource `protecao://catalogo-regional` disponibiliza a primeira cobertura municipal.

**Limites:** esta carga inicial cobre somente São Paulo (capital), não o estado inteiro nem o Brasil. Não calcula proximidade, não garante disponibilidade de atendimento e não publica endereços de abrigos sigilosos. Confirme funcionamento antes do deslocamento. Em perigo imediato, 190; orientação, 180.


## Cursos e capacitações gratuitas para mulheres

Foi adicionado o módulo MCP `buscar_cursos_programas_para_mulheres(uf)`, o resource `capacitacao://programas-gratuitos` e o prompt `orientar_inscricao_cursos_mulheres`.

A primeira lista inclui o curso Ela Empreende! (Qualifica SP), módulos de Educação Financeira para Mulheres Empreendedoras (MDS) e o Programa Mulheres Mil (MEC). Em 03/11/2026, a Agência Gov informou 230 vagas previstas em 11 cursos do Mulheres Mil para novembro e dezembro, em MG, PE, PR, ES, RN e BA. O agente direciona ao Painel de Oportunidades do Pronatec e deixa claro que a previsão de oferta não garante vaga ou inscrição aberta. Cada oportunidade informa público, formato, fonte oficial, gratuidade e status. A ferramenta não solicita credenciais nem documentos; eventual login gov.br ocorre somente no portal externo oficial.


## Governança de atualização do catálogo de proteção

Cada registro do catálogo de proteção possui data de verificação e prazo de revisão editorial calculado em 90 dias. A ferramenta `buscar_servicos_protecao_por_localidade` oculta por padrão registros com data ausente/inválida ou prazo vencido e informa quantos foram omitidos. O parâmetro `incluir_registros_vencidos=true` existe para auditoria e retorna os registros marcados como `expired` ou `needs_review`; eles não devem ser apresentados como contatos atuais. O prazo é um alerta para revisão humana, não uma validação automática de que o serviço continua funcionando.

A data `review_due_date` é armazenada no JSON e calculada novamente pela lógica do serviço. Antes de adicionar ou renovar um registro, verificar a página institucional, contato, endereço público, horário, cobertura e gratuidade. Não divulgar endereço de acolhimento sigiloso.


## Assistência jurídica — integração MCP e canal paulista verificado

A ferramenta `orientar_assistencia_juridica_gratuita(uf, municipio)`, o resource `juridico://assistencia-gratuita` e o prompt `orientar_busca_defensoria_mulher` estão registrados no servidor MCP.

Para SP, a resposta apresenta o canal estadual da Defensoria Pública: **0800 773 4340**, gratuito, segunda a sexta das 7h às 19h em dias úteis; fins de semana e feriados das 7h às 12h, apenas casos urgentes pelo site com a assistente virtual Júlia. O atendimento exige agendamento prévio. A Carta de Serviços do Estado, atualizada em 09/09/2026, informa que não é preciso apresentar documentos para solicitar o serviço; isso não dispensa documentos que possam ser necessários posteriormente. A ferramenta também aponta a página do NUDEM/SP, sem inventar telefone direto não confirmado.

Fontes: https://servicos.sp.gov.br/fcarta/2C493B4D-3542-4441-9DD4-60E7285C8DAB ; https://www.defensoria.sp.def.br/institucional/enderecos-e-telefones ; https://www.defensoria.sp.def.br/nucleos-especializados/pagina-inicial-nucleos-especializados/direitos-das-mulheres/redes-de-atendimento/violencia-domestica-e-familiar

As ferramentas de ONGs e coletivos também estão registradas no servidor MCP: `orientar_busca_ongs_coletivos_mulheres(uf, municipio)`, resource `comunidade://ongs-e-coletivos` e prompt `orientar_validacao_ong_feminina`. Elas retornam fontes de descoberta e checklist de validação; não afirmam que uma organização local foi confirmada.



## Assistência jurídica — contatos estaduais ampliados

O módulo `orientar_assistencia_juridica_gratuita(uf, municipio)` agora inclui informações estaduais verificadas para SP, BA e PR, além de diretórios nacionais para as demais UFs:

- **Bahia:** Disque Defensoria 129 ou 0800 071 3121, ligação gratuita, segunda a sexta das 8h às 17h (página estadual atualizada em 17/07/2026).
- **Paraná:** Defensoria Pública (41) 99123-1961; NUDEM (41) 99285-8134 e nudem@defensoria.pr.def.br, de segunda a sexta das 10h às 17h, somente com agendamento.
- **São Paulo:** canal estadual 0800 773 4340 e NUDEM com encaminhamento pelo canal geral, conforme as ressalvas já documentadas.

A cobertura específica não representa atendimento nacional completo. Os dados não garantem vaga ou disponibilidade imediata; confirmar critérios e fluxo diretamente com o órgão. Fontes, datas e limitações estão detalhadas em `docs/AGENTE_ELAS_CONECTADAS.md`.


## Assistência psicossocial e social gratuita

A orientação jurídica também aponta para o **CREAS**, serviço público e gratuito do SUAS que atende pessoas e famílias com direitos violados, incluindo violência física, psicológica e sexual. O MDS disponibiliza localizador oficial por município; se não houver CREAS local, a orientação oficial é procurar a assistência social da prefeitura. A ferramenta não presume endereço ou vaga.

Contatos especializados adicionais registrados: **Minas Gerais** — NUDEM/Belo Horizonte, (31) 98475-2616 e (31) 98239-8863, 11h–17h; **Pernambuco** — NUDEM, WhatsApp (81) 99488-3765, atendimento inicial exclusivamente por mensagem e respostas por ordem de chegada. Escopo geográfico e condições estão na documentação técnica.


### Ferramenta MCP dedicada — CREAS
- Tool: `orientar_acesso_creas(uf, municipio)`
- Resource: `assistencia://creas`
- Prompt: `orientar_busca_apoio_psicossocial`
- Usa o localizador oficial do MDS e informa que o CREAS é público e gratuito. Não inventa unidades, vagas ou disponibilidade.


## Acolhimento, idioma e canais urgentes

Na primeira resposta, o agente deve acolher sem julgamento, informar **190** para perigo imediato e **Ligue 180** para orientação e atendimento sobre violência contra a mulher (gratuito, 24 horas), e perguntar qual idioma a usuária prefere. Para não atrasar a ajuda, começa em português e muda quando a usuária indicar outro idioma. Informações públicas nunca dependem de cadastro, login, e-mail, senha, CPF ou relato detalhado. Deve solicitar somente a localização mínima necessária, oferecer município/UF como alternativa ao CEP e nunca divulgar endereços sigilosos de abrigos.


## ONGs e iniciativas de apoio gratuito a mulheres

A ferramenta MCP `orientar_busca_ongs_coletivos_mulheres(uf, municipio)` passou a apresentar iniciativas com informações institucionais verificadas, além de fontes de descoberta:

- **TamoJuntas:** organização feminista composta por mulheres profissionais voluntárias; declara oferecer assessoria jurídica, psicológica e social gratuita a mulheres em situação de violência e vulnerabilidade. A página institucional informa atendimento presencial em Salvador, Recife, São Paulo e Rio de Janeiro, além de atuação voluntária em outras regiões. O agente apresenta e-mail por estado quando publicado, mas não promete disponibilidade no município nem atendimento imediato.
- **Mapa do Acolhimento:** conecta mulheres cis e trans, maiores de 18 anos, de baixa renda e residentes no Brasil, que passaram por violência de gênero, a profissionais voluntárias para acolhimento psicológico e jurídico gratuito. A solicitação ocorre em formulário externo; isso não cria exigência de cadastro no Elas Conectadas. O agente não preenche o formulário nem coleta dados pessoais.

**Limite:** a inclusão significa que a organização declara publicamente a oferta e o público descritos; não confirma vaga, prazo de resposta ou profissional disponível. A usuária deve contatar a organização pelo canal institucional. Fontes verificadas em 03/11/2026: [TamoJuntas — atendimento](https://tamojuntas.org.br/elementor-2722/), [TamoJuntas — contatos](https://tamojuntas.org.br/inicio/), [Mapa do Acolhimento — peça ajuda](https://www.mapadoacolhimento.org/atendimento/).


## Segurança digital e acolhimento especializado

O diretório de iniciativas verificadas agora inclui a **Maria d'Ajuda**, linha de ajuda feminista e gratuita da MariaLab para mulheres, pessoas não binárias, pessoas LGBTQIA+ e organizações da América Latina que enfrentam ameaças digitais. O canal institucional publicado é **sos@mariadajuda.org**; a página informa retorno em até dois dias, prazo que deve ser confirmado diretamente com a equipe. O escopo é segurança digital e não substitui emergência policial, assistência jurídica ou atendimento psicológico.

A **Marias da Internet** aparece em uma seção separada de iniciativas especializadas cuja gratuidade não foi confirmada nas páginas institucionais consultadas. Por isso, o agente não pode apresentá-la como serviço gratuito até validar esse ponto diretamente.

**Limite importante:** o Helpline da SaferNet é voltado a crianças e adolescentes; a página oficial informa que adultos não são elegíveis para orientação individual. Não o indicar como canal geral para mulheres adultas.

Fontes institucionais: https://mariadajuda.org/ ; https://www.mariasdainternet.com.br/ ; https://new.safernet.org.br/helpline


## Priorização territorial das ONGs e iniciativas

A ferramenta de ONGs agora classifica os resultados conforme a localização informada, sem excluir opções online:

- Primeiro: atendimento presencial publicado para a cidade informada (TamoJuntas: Salvador, Recife, São Paulo e Rio de Janeiro).
- Em seguida: iniciativas com escopo online nacional ou latino-americano (Mapa do Acolhimento e Maria d'Ajuda), sempre com critérios e limites de disponibilidade.
- Depois: contato estadual publicado sem confirmação de atendimento presencial na cidade, ou orientação/encaminhamento para outras localidades.
- Sem município/UF, o agente não presume presença local.

A classificação usa os campos `locality_match`, `locality_priority` e `locality_evidence`. Ela não calcula distância, não confirma vaga ou disponibilidade e não deve ser interpretada como garantia de atendimento. A lista mantém as opções online relevantes, mas coloca a cobertura local comprovada primeiro.

Fonte institucional da TamoJuntas para cidades presenciais e orientações a outras localidades: https://tamojuntas.org.br/elementor-2722/


## Expansão regional do catálogo de proteção — Rio de Janeiro e Recife

Em 04/11/2026, foram adicionados ao catálogo regional três registros com atendimento gratuito declarado em páginas oficiais municipais:

- **Rio de Janeiro/RJ:** CEAM Chiquinha Gonzaga e CEAM Tia Gaúcha. A Prefeitura informa atendimento gratuito e esclarece que não é necessário boletim de ocorrência para buscar ajuda nos CEAMs. Os horários não foram reproduzidos porque a página oficial consultada não os especifica.
- **Recife/PE:** Centro de Referência Clarice Lispector. A Prefeitura confirma gratuidade, equipe multidisciplinar, endereço, telefone e atendimento 24 horas. Também são publicados o Liga Mulher 0800 281 0107 e o WhatsApp de plantão 24h (81) 99488-6138.

### Bahia — serviço oficial identificado, custo não cadastrado como gratuito

A Secretaria de Políticas para as Mulheres da Bahia mantém páginas oficiais atualizadas em 06/10/2026 sobre a Casa da Mulher Brasileira de Salvador e os CRAMs Loreta Valadares, Irmã Dulce e Arlete Magalhães. As páginas consultadas apresentam endereços e contatos, mas não afirmam de forma inequívoca a gratuidade de cada atendimento. Por isso, esses registros ainda não foram marcados como gratuitos nem inseridos na lista recomendável de serviços gratuitos. A próxima validação deverá confirmar o custo e os horários diretamente com as unidades ou em fonte oficial que os declare.

Fontes oficiais:
- Rio de Janeiro — CEAMs: https://mulher.prefeitura.rio/centro-especializado-de-atendimento-a-mulher/
- Recife — Centro Clarice Lispector: https://www2.recife.pe.gov.br/servico/centro-de-referencia-clarice-lispector
- Recife — rede de serviços e canais: https://www2.recife.pe.gov.br/pagina/secretaria-da-mulher
- Bahia — Casa da Mulher Brasileira: https://www.ba.gov.br/mulheres/7117/casa-da-mulher-brasileira
- Bahia — CRAMs: https://www.ba.gov.br/mulheres/7119/crams

**Limites:** a cobertura adicionada é municipal (Rio de Janeiro e Recife), não estadual. A ausência de registro gratuito para Salvador não significa ausência de serviço; significa apenas que a gratuidade ainda não foi confirmada com o padrão de evidência do catálogo. Nenhum endereço sigiloso foi incluído. A validade de 90 dias é editorial e não garante funcionamento ou disponibilidade.


## Expansão territorial — Bahia e Pernambuco

Em 04/11/2026, o catálogo foi ampliado com **30 referências municipais na Bahia** e **32 em Pernambuco**, a partir de diretórios oficiais estaduais:

- Bahia: lista estadual de CRAMs/centros de atendimento, com endereços e telefones publicados em 06/10/2026.
- Pernambuco: Portal da Transparência estadual, com CRM/CEAM por região, endereço, telefone e horários informados.

**Importante sobre gratuidade:** as páginas estaduais consultadas não declaram explicitamente a gratuidade individual de cada unidade. Por isso, esses registros usam `free: null`, `cost_status: not_confirmed_by_official_source` e `recommendation_status: cost_confirmation_required`. Eles não são contados como serviços gratuitos e o agente deve priorizar `free: true`. Só podem ser apresentados como referências para confirmação direta, nunca como atendimento gratuito confirmado.

Fontes:
- Bahia: https://www.ba.gov.br/mulheres/7119/crams
- Pernambuco: https://transparencia.pe.gov.br/gestao-estadual/informacao-protecao-e-atendimento-as-mulheres/protecao-e-atendimento-as-mulheres/

A cobertura é municipal conforme as unidades listadas; não representa todos os municípios desses estados. A presença em diretório não confirma vaga, funcionamento no momento da consulta ou disponibilidade de equipe. Contatos e horários devem ser confirmados antes do deslocamento.


## Cobertura nacional — 13 Casas da Mulher Brasileira

O catálogo agora inclui as 13 Casas da Mulher Brasileira (12 registros novos; São Paulo já constava no catálogo) que o Ministério das Mulheres listou como em funcionamento em agosto de 2026: Brasília/Ceilândia (DF), Campo Grande (MS), Salvador (BA), Fortaleza (CE), São Luís (MA), Teresina (PI), Aracaju (SE), Macapá (AP), Ananindeua (PA), Boa Vista (RR), Palmas (TO), São Paulo (SP) e Curitiba (PR). A fonte nacional confirma funcionamento 24 horas, todos os dias, mas não declara explicitamente a gratuidade das Casas. A declaração de gratuidade na mesma página refere-se ao Ligue 180. Por isso, as Casas estão marcadas com `free: null` e não são recomendadas como gratuitas até confirmação.

Fonte oficial: https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/agosto-defeso-eleitoral/casa-da-mulher-brasileira-como-funciona-o-atendimento-e-onde-encontrar-uma-unidade

O endereço está cadastrado apenas para as Casas da Mulher Brasileira listadas publicamente. Nenhum endereço de abrigo sigiloso é divulgado. A lista de unidades em funcionamento foi publicada em agosto de 2026 e deve ser revalidada antes do prazo editorial.


### Distrito Federal — quatro Centros de Referência com gratuidade confirmada

Foram adicionados quatro Centros de Referência da Mulher Brasileira no DF: Recanto das Emas, Sol Nascente, São Sebastião e Sobradinho II. O Governo do Distrito Federal confirma atendimento gratuito, sem necessidade de agendamento, com telefones e endereços publicados. Horário informado: segunda a sexta, das 9h às 18h.

Fonte oficial: https://www.gdfsaude.df.gov.br/web/guest/w/ef-centros-oferecem-atendimento-gratuito-a-mulheres-em-situacao-de-vulnerabilidade?p_l_back_url=%2Fweb%2Fguest%2Ftopicos%3Fsort%3DcreateDate-%26tag%3DEspa%25C3%25A7o%2BPr%25C3%25B3-Mulher&p_l_back_url_title=T%C3%B3picos


## Expansão territorial — Acre, Goiás, Piauí e Espírito Santo

Em 04/11/2026, foram adicionadas oito referências municipais de Centros de Referência da Mulher Brasileira, com base em páginas oficiais do Governo Federal, da Secretaria de Estado da Mulher do Acre e de prefeituras:

- **Acre:** Cruzeiro do Sul e Brasiléia, com telefones publicados pela Secretaria de Estado da Mulher.
- **Goiás:** Águas Lindas de Goiás, Jataí, Cidade Ocidental e Santo Antônio do Descoberto. Para Jataí há endereço publicado; Cidade Ocidental tem contato e horário em página municipal.
- **Piauí:** São Raimundo Nonato, com endereço publicado e atendimento regional informado para 18 municípios do Território da Serra da Capivara.
- **Espírito Santo:** Cariacica, com endereço, telefone e horário publicados pelo Ministério das Mulheres.

**Gratuidade:** as fontes consultadas não confirmam expressamente que cada atendimento dessas oito unidades seja gratuito. Todos os registros usam `free: null`, `cost_status: not_confirmed_by_official_source` e `recommendation_status: cost_confirmation_required`. Não devem ser apresentados como serviços gratuitos confirmados.

Fontes oficiais: [Secretaria da Mulher do Acre](https://semulher.ac.gov.br/voce-nao-esta-sozinha/); [Ministério das Mulheres — Águas Lindas](https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2025/outubro/em-aguas-lindas-de-goias-marcia-lopes-inaugura-centro-de-referencia-da-mulher-brasileira); [Ministério das Mulheres — Jataí](https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2024/marco/em-goias-municipio-de-jatai-ganha-primeiro-centro-de-referencia-da-mulher-brasileira-nesta-sexta-feira-8); [Prefeitura de Cidade Ocidental](https://cidadeocidental.go.gov.br/centro-de-referencia-da-mulher-brasileira/); [Ministério das Mulheres — CRMBs em Goiás](https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/junho/ministra-marcia-lopes-visita-rede-de-protecao-as-mulheres-em-cidade-ocidental-go); [Ministério das Mulheres — São Raimundo Nonato](https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/janeiro/sao-raimundo-nonato-inaugura-primeiro-centro-de-referencia-da-mulher-brasileira); [Ministério das Mulheres — Cariacica](https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/outubro-defeso-eleitoral/centro-de-referencia-da-mulher-brasileira-em-cariacica-es-oferecera-atendimento-a-mulheres-em-situacao-de-violencia).

### Como interpretar a cobertura nacional

O catálogo local não equivale a uma base nacional completa. O Ministério das Mulheres informa que o Painel da Rede permite pesquisar serviços por estado e município e reúne delegacias, Defensorias, CRAM/CEAM, acolhimento, saúde, Casas da Mulher Brasileira e outros pontos de atenção. A ferramenta MCP de consulta ao painel continua sendo um encaminhamento oficial, não uma importação automática dos registros. Ausência de unidade no catálogo não significa ausência de serviço no município.

Fonte: https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento


## Expansão municipal complementar — Rio Grande do Norte, Rio Grande do Sul e Santa Catarina

Em 04/11/2026, foram incluídas quatro referências municipais adicionais:
- **Mossoró/RN:** Centro de Referência da Mulher Brasileira, cuja operação é citada pelo Ministério das Mulheres em publicação de março de 2026.
- **Porto Alegre/RS:** Centro de Referência da Mulher Vânia Araújo Machado, com Escuta Lilás, telefone, WhatsApp, endereço e horário publicados pelo Governo do Estado.
- **Florianópolis/SC:** CREMV, com endereço, telefone e e-mail em página institucional municipal.
- **Sapucaia do Sul/RS:** Centro de Referência da Mulher, com endereço, telefone e horário em página oficial municipal.

A gratuidade individual não foi explicitamente confirmada pelas fontes utilizadas. Os quatro registros permanecem com `free: null` e custo não confirmado. Não os apresentar como serviços gratuitos confirmados.

Fontes: https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/marco/tenda-lilas-leva-acolhimento-e-informacao-sobre-enfrentamento-a-violencia-contra-as-mulheres-em-sergipe-e-no-rio-grande-do-norte ; https://www.estado.rs.gov.br/sexta-conferencia-estadual-de-politicas-para-as-mulheres-define-tres-propostas-e-elege-91-delegadas-para-a-etapa-nacional ; https://devportal.pmf.sc.gov.br/entidades/saude/index.php?cms=raivs&menu=6&submenuid=dyn-153 ; https://www.sapucaiadosul.rs.gov.br/telefones-uteis/


## Atualização territorial — UFs antes sem referências locais (04/11/2026)

Foram incorporadas referências de atendimento em **Alagoas, Amazonas, Mato Grosso, Minas Gerais, Paraíba e Rondônia**. A inclusão reduz as lacunas estaduais, mas não significa cobertura de todos os municípios.

- **Alagoas:** CEAM de Maceió (gratuidade expressamente indicada no Portal Alagoas Digital) e Espaço Viva Mulher/CRAMSV de Arapiraca (custo não confirmado na carta municipal).
- **Amazonas:** CREAM e seis unidades SAPEM em Manaus; seis SAMIC no interior (Itacoatiara, Humaitá, Maués, Tefé, Parintins e Tabatinga). As páginas da SEJUSC descrevem atendimento psicossocial e encaminhamentos para mulheres; a gratuidade individual não foi explicitamente confirmada.
- **Mato Grosso:** delegacias especializadas em Cuiabá, Cáceres, Rondonópolis, Sinop, Tangará da Serra e Várzea Grande, a partir do diretório estadual. O próprio diretório lista horário comercial para os serviços; confirme antes de ir. 
- **Minas Gerais:** CERNA, em Belo Horizonte, com atendimento gratuito declarado pelo Governo de Minas e modalidades presencial/virtual para mulheres do estado.
- **Paraíba:** CRAM Ednalva Bezerra, em João Pessoa, e CRAM de Campina Grande. O custo não foi declarado expressamente nas fontes utilizadas e permanece pendente de confirmação.
- **Rondônia:** CRAM de Porto Velho, com endereço e telefone publicados pela Prefeitura em agosto de 2026; a gratuidade não foi expressamente confirmada.

### Fontes oficiais e institucionais consultadas
- Alagoas — Portal Alagoas Digital (CEAM Maceió): https://alagoasdigital.al.gov.br/servico/3019
- Alagoas — Carta de Serviços de Arapiraca (Espaço Viva Mulher): https://cartadeservicos.arapiraca.al.gov.br/servico/159
- Amazonas — SEJUSC (CREAM, SAPEM e SAMIC): https://www.sejusc.am.gov.br/mulheres/
- Mato Grosso — Portal Mato Grosso em Defesa das Mulheres (diretório de atendimento): https://mulher.mt.gov.br/atendimentos
- Minas Gerais — Governo de Minas (CERNA): https://www.mg.gov.br/servico/solicitar-atendimento-no-centro-risoleta-neves-de-atendimento-mulheres-cerna
- Paraíba — Observatório do Feminicídio da UEPB (rede de atendimento): https://observatoriodofeminicidio.uepb.edu.br/rede-de-atendimento-as-mulheres-em-situacao-de-violencia-domestica-e-sexual/
- Paraíba — Prefeitura de Campina Grande (CRAM): https://coordenadoriadamulher.campinagrande.pb.gov.br/?page_id=208
- Rondônia — Prefeitura de Porto Velho (CRAM, notícia de 14/08/2026): https://www.portovelho.ro.gov.br/noticias/57903

**Gratuidade:** apenas CEAM Maceió e CERNA/MG foram marcados `free: true` nesta rodada, porque suas fontes declaram expressamente que o serviço não tem custo/é gratuito. Os demais foram mantidos com `free: null` e custo não confirmado. O agente não pode apresentá-los como opções gratuitas confirmadas.

**Limites de cobertura:** os registros de Mato Grosso e Amazonas são serviços especializados e centros em municípios específicos; não representam todos os municípios desses estados. Para municípios sem unidade local curada, manter o encaminhamento ao Painel oficial da Rede do Ligue 180: https://www.gov.br/mulheres/pt-br/ligue180/painel-da-rede-de-atendimento.


### Atualização de Rondônia — 04/11/2026

Foram adicionadas oito referências de Delegacias Especializadas em Atendimento à Mulher no diretório oficial da Polícia Civil de Rondônia: Porto Velho, Ariquemes, Cacoal, Guajará-Mirim, Jaru, Ji-Paraná, Rolim de Moura e Vilhena. A página publica telefones e e-mails, mas não endereços textuais nem horários específicos para essas unidades; por isso, esses campos não foram inventados e a orientação é confirmar localização e funcionamento diretamente com a Polícia Civil. A gratuidade não foi expressamente confirmada na fonte.

Fonte: https://www.pc.ro.gov.br/unidades-policiais/

O registro do CREAM de Manaus também foi corrigido conforme o diretório da SEJUSC: endereço Avenida Presidente Kennedy, 39, Educandos, contatos telefônicos e horário de segunda a sexta, 8h às 17h. A gratuidade permanece não confirmada.

Fonte: https://www.sejusc.am.gov.br/mulheres/


### Revisão de fontes oficiais — 04/11/2026

O catálogo foi ampliado com cinco referências de núcleos/delegacias especializados em Mato Grosso, nos municípios de Nobres, Nova Mutum, Nova Xavantina, Querência e Alto Araguaia. A fonte estadual informa endereço, telefone, e-mail e horário comercial para os registros. A gratuidade não é declarada expressamente e permanece não confirmada.

O registro do Centro de Referência da Mulher Brasileira de Cariacica/ES foi revalidado com a notícia oficial de inauguração de 09/10/2026: Rua Rio Branco, 446, bairro Rio Branco; telefone (27) 3354-5565; segunda a sexta, 8h–18h. A publicação confirma atendimento psicológico, social e orientação jurídica, mas a gratuidade individual não é explicitada.

Fontes:
- Mato Grosso: https://mulher.mt.gov.br/atendimentos
- Cariacica/ES: https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2026/outubro-defeso-eleitoral/centro-de-referencia-da-mulher-brasileira-em-cariacica-es-oferecera-atendimento-a-mulheres-em-situacao-de-violencia

O catálogo agora contém 171 registros em 27 UFs: 47 com gratuidade expressamente confirmada e 124 com custo não confirmado. A cobertura municipal continua parcial.


### Ampliação em lote — Amazonas e Mato Grosso (04/11/2026)

Foram adicionadas 19 referências a partir de diretórios oficiais:
- Amazonas: SAMIC de Barcelos. A página da SEJUSC informa endereço, mas não publica telefone para essa unidade; o campo permanece sem telefone. O serviço oferece atendimento psicológico/social e encaminhamentos nos municípios listados pela Secretaria.
- Mato Grosso: 18 referências de núcleos da Patrulha Maria da Penha e do Organismo de Políticas para Mulheres em Juína, Luciara, Novo Horizonte do Norte, Novo Santo Antônio, Paranatinga, Porto Alegre do Norte, Porto dos Gaúchos, Poxoréu, São Félix do Araguaia, São José do Xingu, Sapezal, Campo Novo do Parecis, Canabrava do Norte, Canarana, Campo Verde, Tapurah, Santa Terezinha e Nova Xavantina.

As referências de Patrulha Maria da Penha não são apresentadas como plantões abertos ou serviços de emergência: a orientação é confirmar área de cobertura, critérios e disponibilidade diretamente com o contato publicado. Nenhuma dessas 19 referências foi marcada como gratuita, pois as páginas consultadas não declaram expressamente a gratuidade.

Fontes oficiais:
- Amazonas/SEJUSC: https://www.sejusc.am.gov.br/mulheres/
- Mato Grosso: https://www.mulher.mt.gov.br/atendimentos

O catálogo contém agora 195 registros em 27 UFs e 142 combinações de município/UF. São 47 registros com gratuidade expressamente confirmada e 148 com custo não confirmado. A cobertura municipal continua parcial.


### Expansão municipal — Alagoas e Paraíba (04/11/2026)

Foram adicionadas cinco referências:
- Maceió/AL: Área Lilás do Hospital da Mulher (24h) e Sala Lilás do Complexo de Delegacias Especializadas (7h–19h diariamente).
- Arapiraca/AL: Área Lilás do Hospital de Emergência do Agreste (24h).
- Delmiro Gouveia/AL: Sala Lilás no CISP (7h–19h diariamente; endereço de rua não publicado na fonte consultada).
- Bayeux/PB: CRAM, com endereço identificado em publicação do Diário Oficial de 01/05/2026; telefone, horário e início efetivo do atendimento não confirmados na publicação. Confirmar abertura antes de orientar deslocamento.

O CERNA de Belo Horizonte/MG já constava no catálogo e foi revalidado nesta rodada: o Portal MG confirma atendimento gratuito, presencial ou virtual, para mulheres de todo o estado.

Fontes oficiais:
- SESAU Alagoas: https://www.saude.al.gov.br/rede-de-atencao-as-violencias/
- Prefeitura de Arapiraca (publicação de agosto/2026): https://web.arapiraca.al.gov.br/2026/08/arapiraca-abre-programacao-do-agosto-lilas-reunindo-esporte-e-conscientizacao-com-treinao-sextou/
- Diário Oficial da Paraíba (01/05/2026): https://auniao.pb.gov.br/servicos/doe/2026/maio/diario-oficial-01-05-2026-portal.pdf
- Portal MG — CERNA: https://www.mg.gov.br/servico/solicitar-atendimento-no-centro-risoleta-neves-de-atendimento-mulheres-cerna

O catálogo contém 195 registros em 27 UFs e 143 combinações município/UF. São 47 registros com gratuidade expressamente confirmada e 148 com custo não confirmado. A cobertura municipal continua parcial.


### Expansão municipal — Mato Grosso e Alagoas (04/11/2026)

Foram adicionadas 13 referências:
- **Mato Grosso:** Barra do Bugres (núcleo especializado), Barra do Garças (DEAM), Brasnorte (Departamento da Mulher), Lucas do Rio Verde (DEAM e núcleo especializado), Matupá, Peixoto de Azevedo, Pontes e Lacerda, Primavera do Leste e Vera (unidades especializadas).
- **Alagoas:** Rio Largo (Hospital Dr. Ib Gatto Falcão), Porto Calvo (Hospital Regional do Norte) e Maceió (Sala Lilás do HGE).

No caso de Rio Largo e Porto Calvo, a fonte estadual confirma o ponto de acolhimento hospitalar, mas não publica endereço de rua, telefone ou horário individual. Esses campos permanecem sem preenchimento, sem inferências. Para as unidades de Mato Grosso, o diretório estadual lista horário comercial; isso não deve ser confundido com plantão 24h. Os registros não foram classificados como gratuitos porque a fonte não declara expressamente a gratuidade.

Fontes oficiais:
- Portal Mato Grosso em Defesa das Mulheres — diretório de atendimentos: https://mulher.mt.gov.br/atendimentos
- SESAU Alagoas — Rede de Atenção às Violências: https://www.saude.al.gov.br/rede-de-atencao-as-violencias/
- SESAU Alagoas — notícia sobre pontos no interior, atualizada em 25/02/2026: https://www.saude.al.gov.br/rede-de-atencao-as-violencias-promove-acoes-socioeducativas-no-porto-de-maceio/

**Métricas atuais após a rodada:** 208 registros, 208 IDs únicos, 27 UFs e 154 combinações município/UF. São 47 registros com gratuidade expressamente confirmada e 161 com custo não confirmado. Cobertura municipal parcial; presença em diretório não garante vaga, disponibilidade, funcionamento ininterrupto ou atendimento imediato.


### Expansão estadual — Mato Grosso do Sul (04/11/2026)

Foram adicionadas **40 referências** a partir do diretório oficial estadual "Não Se Cale":
- 11 centros municipais de referência/atendimento à mulher: Jardim, Dourados, Paranaíba, Aquidauana, Corumbá, Coxim, Fátima do Sul, Naviraí, Nova Andradina, Três Lagoas e Rio Brilhante.
- 13 Delegacias de Atendimento à Mulher (DEAMs): Aquidauana, Bataguassu, Campo Grande, Corumbá, Coxim, Dourados, Fátima do Sul, Jardim, Naviraí, Nova Andradina, Paranaíba, Ponta Porã e Três Lagoas.
- 16 pontos do PROMUSE/Programa Mulher Segura vinculados à Polícia Militar: Amambai, Aquidauana, Batayporã, Bonito, Caarapó, Campo Grande, Dourados, Fátima do Sul, Inocência, Jardim, Naviraí, Nova Andradina, Paranaíba, Pedro Gomes, Ponta Porã e Três Lagoas.

Os registros PROMUSE foram classificados como proteção/policiamento especializado, não como delegacia ou plantão de emergência. Os horários não publicados foram deixados sem confirmação. A fonte oficial não declara gratuidade individual para esses serviços; os 40 registros permanecem com custo não confirmado.

Fonte oficial: https://www.naosecale.ms.gov.br/fale-conosco/outros-contatos/

**Métricas após a rodada:** 248 registros, 248 IDs únicos, 27 UFs e 177 combinações município/UF. São 47 registros com gratuidade expressamente confirmada e 201 com custo não confirmado. A cobertura é parcial e a presença em diretório não garante disponibilidade imediata.


### Expansão rápida — organismos municipais e NUDEM em Mato Grosso do Sul (04/11/2026)

Foram adicionadas **49 referências**:
- 48 organismos municipais de políticas para mulheres (coordenadorias, gerências e secretarias) em municípios do estado, com os contatos e endereços publicados pelo portal estadual.
- 1 NUDEM da Defensoria Pública de MS, em Campo Grande. A página oficial informa atendimento jurídico especializado, telefone (67) 3313-4919, e-mail nudem@defensoria.ms.def.br e endereço Avenida Afonso Pena, 3850. A atuação do NUDEM no interior depende de designação excepcional.

Os organismos municipais são portas de orientação institucional, articulação e encaminhamento; não foram descritos como delegacias, abrigos ou plantões de emergência. Horários não publicados permanecem como não informados. Os 48 organismos municipais não tiveram gratuidade individual presumida. A gratuidade do NUDEM está indicada conforme a natureza do serviço da Defensoria Pública.

Fontes:
- Diretório estadual: https://www.naosecale.ms.gov.br/fale-conosco/outros-contatos/
- NUDEM: https://www.naosecale.ms.gov.br/rede-de-apoio/defensoria-publica-de-mato-grosso-do-sul/

**Métricas após esta rodada:** 297 registros, 297 IDs únicos, presença nas 27 UFs, 215 combinações município/UF, 48 registros com gratuidade expressamente confirmada e 249 com custo não confirmado. A cobertura é parcial; os organismos municipais não substituem atendimento emergencial ou especializado.


### Expansão da Paraíba — 04/11/2026

Adicionadas 15 referências a partir de publicações oficiais:
- 12 municípios listados no Informativo nº 1, de março de 2025, do Governo da Paraíba como locais com Delegacia Especializada de Atendimento à Mulher: João Pessoa, Picuí, Sousa, Cajazeiras, Campina Grande, Bayeux, Cabedelo, Guarabira, Santa Rita, Monteiro, Patos e Mamanguape.
- 2 Núcleos de Atendimento à Mulher da Polícia Civil citados no mesmo informativo: Queimadas e Esperança.
- 1 Ronda Maria da Penha em João Pessoa, com contatos municipais divulgados pela Prefeitura.

**Limite de verificação:** o informativo estadual é de março de 2025 e comprova que as unidades foram relacionadas naquele momento, mas não publica endereços, telefones diretos ou horários; por isso, os registros de DEAMs e núcleos ficam marcados como necessidade de reconfirmação operacional. O número 197 é canal estadual da Polícia Civil, não telefone direto das unidades. Não importar endereços e contatos de diretórios antigos.

O Centro de Referência da Mulher Ednalva Bezerra, em João Pessoa, também foi atualizado com base no relatório municipal publicado em 26/12/2025: atendimento presencial na Rua Afonso Campos, 111, de segunda a sexta, 8h–16h; Prefeitura informa atendimento 24h pelo 0800-283-3883 e contatos (83) 98695-3549 e (83) 3213-7359 em dias úteis, 8h–17h. Atendimento remoto em fins de semana e feriados.

Fontes:
- https://paraiba.pb.gov.br/diretas/secretaria-de-desenvolvimento-humano/consultas/Informativo2025n1DiaInternacionaldaMulher2.pdf
- https://www.joaopessoa.pb.gov.br/noticias/prefeitura-registra-315-atendimentos-a-mulheres-vitimas-de-violencia-em-2025/
- https://www.joaopessoa.pb.gov.br/noticias/dia-internacional-pela-eliminacao-da-violencia-contra-as-mulheres-e-marcado-por-reforco-a-rede-de-protecao-e-acoes-de-conscientizacao/

**Métricas após esta rodada:** 312 registros, 312 IDs únicos, 27 UFs, 226 combinações município/UF, 49 registros com gratuidade confirmada e 263 com custo não confirmado. A cobertura segue parcial; os novos registros policiais de PB não devem ser tratados como confirmação de funcionamento atual até reconfirmação direta.


### Expansão da rede de proteção em Minas Gerais — 04/11/2026

Adicionadas três referências em Belo Horizonte com base em publicações oficiais de 2025:
- Delegacia Especializada de Atendimento à Mulher — Rua Rio Grande do Sul, 661, Barro Preto; telefone (31) 3330-5752, conforme Portal MG atualizado em 08/01/2025.
- Delegacia de Plantão Especializada (DEPAM) — entrada pela Avenida Bias Fortes, 1.451, Barro Preto. A Polícia Civil informou o endereço em 06/01/2025; não publicou telefone direto. 197 é canal geral da Polícia Civil.
- Casa da Mulher Mineira — Avenida Augusto de Lima, 1.845, Barro Preto. A Polícia Civil confirmou que permanecia neste endereço em 06/01/2025; a publicação não detalha telefone, horário ou escopo.

Os três registros têm custo não confirmado e exigem confirmação de funcionamento/horário antes do deslocamento. Não foram presumidos serviços, gratuidade ou disponibilidade não publicados.

Fontes:
- https://www.mg.gov.br/instituicao_unidade/delegacia-especializada-de-atendimento-mulher
- https://www.policiacivil.mg.gov.br/site-pc/noticia/exibir?=Delegacias-especializadas-funcionam-em-novo-endere%C3%A7o-na-capital&id=4041323

**Métricas após esta rodada:** 315 registros, 315 IDs únicos, 27 UFs, 226 combinações município/UF, 49 registros com gratuidade confirmada e 266 com custo não confirmado.


### Expansão de Alagoas — delegacias especializadas (04/11/2026)

Adicionadas três referências policiais com base na página oficial da Rede de Atenção às Violências da Secretaria de Estado da Saúde de Alagoas:
- 1ª Delegacia Especializada de Atendimento à Mulher — Complexo de Delegacias Especializadas (CODE), Mangabeiras, Maceió; (82) 3315-4976; funcionamento informado: 24 horas.
- 2ª Delegacia Especializada de Atendimento à Mulher — Rua Antônio Souza Braga, Salvador Lyra, Maceió; (82) 3315-4327; 8h–18h.
- Delegacia da Mulher — Rua São Domingos, Centro, Arapiraca; (82) 3521-6318; 8h–18h.

A página estadual de saúde consultada lista os contatos e horários na seção "Onde essas mulheres podem denunciar?". A gratuidade individual não foi presumida. Os registros representam canais policiais especializados, não atendimento jurídico ou psicossocial.

Fonte oficial:
- https://www.saude.al.gov.br/rede-de-atencao-as-violencias/

**Métricas após esta rodada:** 318 registros, 318 IDs únicos, presença nas 27 UFs, 228 combinações município/UF, 49 registros com gratuidade confirmada e 269 com custo não confirmado.


### Complemento de Alagoas — hospitais de referência (04/11/2026)

Além das três delegacias especializadas, foram cadastrados quatro hospitais que a SESAU/AL lista como referências no atendimento a vítimas de violência sexual:
- Hospital Geral do Estado Prof. Osvaldo Brandão Vilela, Maceió — (82) 3315-3281.
- Hospital da Mulher Dra. Nise da Silveira, Maceió — (82) 3315-1393.
- Hospital Dr. Ib Gatto Falcão, Rio Largo — (82) 3261-2414.
- Hospital de Emergência Daniel Houly, Arapiraca — (82) 3539-8634.

A página estadual informa que os dois primeiros atendem públicos de 0 a 12 anos e maiores de 13 anos; os dois últimos, vítimas de qualquer sexo e idade. O horário específico do serviço hospitalar e a gratuidade individual não foram presumidos; confirmar diretamente com a unidade. Estes registros de saúde são distintos dos pontos de acolhimento da RAV já catalogados.

Fonte oficial:
- https://www.saude.al.gov.br/rede-de-atencao-as-violencias/

**Métricas após o complemento:** 322 registros, 322 IDs únicos, presença nas 27 UFs, 226 combinações município/UF, 49 registros com gratuidade confirmada e 273 com custo não confirmado.


## Capacitação feminina — diretório priorizado

O módulo `WomenTrainingDirectory` foi ampliado com três cursos gratuitos da WoMakersCode / Mais Mulheres em Tech, iniciativa criada por mulheres para mulheres:
- Introdução à Inteligência Artificial — curso online, autoinstrucional e com certificado.
- Como Conseguir um Emprego — currículo, busca de vagas, LinkedIn e entrevistas; online e gratuito.
- Liderança Feminina e Soft Skills — conteúdo gravado, gratuito, online, com certificado e interpretação em Libras.

As páginas dos cursos foram consultadas em 04/11/2026. A página oficial não publica prazo ou quantidade de vagas para os cursos autoinstrucionais; por isso, o agente informa que o conteúdo estava acessível na verificação e orienta confirmar o acesso diretamente na plataforma. O conteúdo de liderança é gravação de bootcamp de 2020, não uma nova turma ao vivo.

A busca agora ordena primeiro as iniciativas de mulheres para mulheres e mantém cursos nacionais disponíveis quando a pesquisa é filtrada por UF. Isso não significa que todos os bootcamps da organização estejam abertos: as turmas com inscrições encerradas continuam fora dos resultados como oportunidades abertas.

Fontes oficiais:
- WoMakersCode — programas: https://www.womakerscode.org/programas
- Introdução à IA: https://www.maismulheres.tech/courses/introducao-inteligencia-artificial
- Como Conseguir um Emprego: https://www.maismulheres.tech/courses/como-conseguir-um-emprego
- Liderança Feminina e Soft Skills: https://www.maismulheres.tech/courses/lideranca-feminina-e-soft-skills
