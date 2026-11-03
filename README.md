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

Projeto em fase de definição e estruturação do MVP. A cobertura nacional e a atualização contínua são objetivos a validar por meio de implementação e testes; não são apresentadas aqui como funcionalidades já concluídas.


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

Foi adicionada a ferramenta MCP orientar_assistencia_juridica_gratuita, o resource juridico://assistencia-gratuita e o prompt orientar_busca_defensoria_mulher. Eles encaminham a usuária aos diretórios do Conselho Nacional de Justiça e do CONDEGE, além do Ligue 180 e do Painel da Rede de Atendimento.

O agente não simula uma busca municipal: a ferramenta retorna links oficiais e instruções para localizar a Defensoria do estado, procurar atendimento à mulher/NUDEM e confirmar critérios diretamente com a instituição. Não solicita CPF, documentos ou relato de violência.
