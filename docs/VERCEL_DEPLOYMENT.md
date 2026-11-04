# Deploy HTTP do Elas Conectadas na Vercel

## Estado desta adaptação

O servidor MCP existente continua funcionando por stdio para desenvolvimento local. A camada HTTP foi adicionada separadamente, usando Streamable HTTP e uma aplicação ASGI Starlette compatível com o runtime Python da Vercel.

- Entry point Vercel: api/index.py
- Endpoint MCP: /api/mcp
- Autenticação: token Bearer obrigatório em todas as requisições MCP.
- Execução serverless: modo HTTP stateless e respostas JSON; não depende de sessões mantidas em memória.
- Allowlist de Host e Origin: obrigatória e explícita; não há wildcard configurado no código.
- Nenhum banco de dados, histórico de conversas ou cadastro foi adicionado.

## Variáveis obrigatórias na Vercel

Configure em Project Settings → Environment Variables, para Preview e Production conforme necessário:

| Variável | Conteúdo |
| --- | --- |
| ELAS_MCP_BEARER_TOKEN | Segredo aleatório forte, exclusivo para este serviço. Nunca commitar ou compartilhar no chat. |
| ELAS_MCP_ALLOWED_HOSTS | Hosts exatos que receberão chamadas, separados por vírgula (ex.: elas-conectadas.vercel.app). |
| ELAS_MCP_ALLOWED_ORIGINS | Origens exatas autorizadas, incluindo esquema (ex.: https://elas-conectadas.vercel.app). |

Não use * nas allowlists. Para domínio customizado, inclua o hostname em ELAS_MCP_ALLOWED_HOSTS e a origem completa em ELAS_MCP_ALLOWED_ORIGINS. Para Preview, configure somente os domínios específicos que realmente serão usados; não libere todos os subdomínios Vercel.

O serviço falha fechado: sem allowlists explícitas a aplicação não inicializa; sem token, o endpoint responde 503; sem token válido, responde 401. O token é comparado em tempo constante e não é retornado em respostas.

## Desenvolvimento local

Instale o projeto e suas dependências:

```bash
python -m pip install -e ".[dev]"
```

Defina as três variáveis obrigatórias com valores locais e execute um servidor ASGI apontando para elas_conectadas_mcp.http_app:app (por exemplo, com Uvicorn instalado no ambiente de desenvolvimento). O endpoint fica em http://localhost:8000/api/mcp.

O comando elas-conectadas-mcp continua iniciando o transporte stdio original. Não altere o cliente MCP local para HTTP sem configurar o endpoint e o token.

## Publicação

1. Conecte o repositório à Vercel usando o runtime Python.
2. Configure as três variáveis obrigatórias antes de testar a função.
3. Crie primeiro um Preview e valide handshake MCP, autenticação e chamadas de ferramentas com dados fictícios.
4. Confirme que a URL pública e o domínio estão cobertos pelas allowlists.
5. Só depois de revisar o Preview, considere promover para Production.

A presença de api/index.py habilita o entrypoint Python ASGI; isso não significa que o projeto já tenha sido implantado ou que exista um projeto Vercel vinculado. A validação final precisa ocorrer em Preview, pois o runtime, o roteamento de subcaminhos e os limites de duração/streaming dependem da plataforma.

## Limites e segurança

- A API HTTP não deve ser exposta sem autenticação.
- O token Bearer é um controle inicial de acesso técnico, não substitui OAuth, gestão de usuários, rotação automatizada ou autorização por escopo.
- Não inclua relatos de violência, dados de saúde, CPF, credenciais gov.br ou localização precisa em logs, testes ou ferramentas externas.
- Não cadastre endereços sigilosos de abrigos.
- Vercel Functions são efêmeras; esta implementação não promete sessões duráveis, notificações em tempo real ou armazenamento.
- O frontend público, a experiência de busca por CEP/município e a política de CORS para navegador serão tratados em uma etapa separada. Não existe interface web nesta alteração.

## Referências oficiais

- https://vercel.com/docs/functions/runtimes/python
- https://py.sdk.modelcontextprotocol.io/run/asgi/
- https://py.sdk.modelcontextprotocol.io/run/deploy/
