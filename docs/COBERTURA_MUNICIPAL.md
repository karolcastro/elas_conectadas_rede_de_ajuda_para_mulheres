# Expansão de cobertura municipal

## Objetivo

Mapear a cobertura do catálogo de proteção em relação à lista oficial de municípios do IBGE, identificar lacunas de cadastro e orientar a pesquisa de fontes municipais. O mapa não presume que um serviço inexista quando ainda não está cadastrado.

## Implementação desta etapa

- Serviço: `src/elas_conectadas_mcp/services/municipal_coverage.py`.
- Ferramenta MCP: `auditar_cobertura_municipal(uf=None, limite_municipios_sem_cadastro=100)`.
- Fonte territorial: API oficial de Localidades do IBGE, consultada em tempo de execução.
- Fonte de serviços: catálogo curado `data/servicos_protecao.json`.
- Testes: `tests/test_municipal_coverage.py`.

## Metodologia

1. Consultar a lista de UFs no IBGE.
2. Para cada UF selecionada, consultar os municípios oficiais e seus códigos IBGE.
3. Ler o catálogo incluindo registros expirados para fins de auditoria.
4. Considerar como cobertura local somente registros com `catalog_status=verified` e município correspondente.
5. Não considerar registros estaduais ou nacionais como unidade local; eles são contabilizados separadamente.
6. Exibir quantidade total, municípios com e sem registro local válido, percentual e amostra limitada das lacunas.

## Limites e salvaguardas

- Município sem registro significa lacuna do catálogo, não inexistência de atendimento.
- A revisão válida do catálogo é controle editorial, não confirmação automática de funcionamento.
- A auditoria não confirma gratuidade, agenda, elegibilidade ou disponibilidade.
- Registros estaduais e nacionais não são tratados como cobertura municipal.
- A amostra de municípios sem registro é limitada por padrão a 100; o limite aceito é de 0 a 500.
- A ferramenta não coleta CEP, endereço residencial ou dados pessoais da usuária.

## Como utilizar

- Brasil: `auditar_cobertura_municipal()`
- Uma UF: `auditar_cobertura_municipal(uf="SP")`
- Amostra maior: `auditar_cobertura_municipal(uf="SP", limite_municipios_sem_cadastro=300)`

## Próxima etapa após a auditoria

Usar os resultados para priorizar a pesquisa documental por UF e município. Cada novo serviço deve ser validado em fonte institucional, com contato, endereço público quando aplicável, abrangência, gratuidade e data de verificação. Abrigos sigilosos nunca terão endereço publicado. Não realizar carga em massa de nomes ou contatos sem validação individual.

## Critérios de aceite

- A lista de municípios vem do IBGE, não de uma planilha manual.
- Filtro por UF funciona e rejeita siglas inválidas.
- Registro municipal vencido não conta como cobertura válida.
- Registro estadual/nacional não conta como cobertura local.
- Resultado apresenta metodologia e limites para impedir conclusões indevidas.
- Testes automatizados cobrem agregação, filtro e validação de parâmetros.


## Fila de pesquisa municipal

A segunda entrega adiciona:

- Serviço: método `MunicipalCoverageService.research_queue()`.
- Ferramenta MCP: `gerar_fila_pesquisa_municipal(uf=None, limite=100, offset=0)`.
- Paginação: limite de 1 a 500 itens por chamada e deslocamento a partir de zero.
- Cada item informa município, UF, código IBGE, situação da pesquisa, referências locais pendentes de revisão e próximas ações de validação.
- A ordenação é determinística por UF e nome do município.

A fila contém municípios sem registro local válido. Registros vencidos ou pendentes não são tratados como cobertura confirmada. A prioridade alta indica apenas que a pesquisa documental ainda precisa ser feita; não representa risco, vulnerabilidade ou urgência da população. A fila não cadastra nem recomenda serviços automaticamente.

Exemplos:

- Brasil, primeira página: `gerar_fila_pesquisa_municipal()`
- São Paulo: `gerar_fila_pesquisa_municipal(uf="SP")`
- Próxima página: `gerar_fila_pesquisa_municipal(uf="SP", limite=100, offset=100)`

Cada instituição encontrada deve passar por validação individual em fonte institucional antes de entrar no catálogo: existência, escopo, contato, endereço público quando aplicável, gratuidade, critérios, funcionamento e data de verificação. Endereços sigilosos de acolhimento não devem ser publicados.
