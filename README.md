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
