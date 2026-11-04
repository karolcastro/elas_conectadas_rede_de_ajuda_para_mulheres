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

Projeto em desenvolvimento com servidor MCP, catálogo nacional de canais oficiais, catálogo regional inicial de São Paulo capital, diretório inicial de capacitações e conectores de território/saúde. A cobertura regional ainda é parcial; a busca não calcula distância e não confirma disponibilidade operacional. Consulte a documentação para limites e status de cada integração.


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
