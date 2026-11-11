# Arquitetura de segurança — Elas Conectadas

**Status:** baseline arquitetural e critérios de liberação. Este documento não é um laudo de pentest nem certifica uma implantação.

## 1. Objetivo e limite de responsabilidade

Permitir que ONGs, coletivos e instituições divulguem o endereço HTTPS oficial do Elas Conectadas sem instalar código, conceder acesso aos seus sistemas ou incorporar conteúdo ativo de terceiros.

A publicação de um link HTML comum cria uma navegação do site da ONG para o Elas Conectadas. Por si só, isso não concede ao Elas Conectadas acesso ao servidor, banco de dados, cookies ou painel administrativo da ONG. O risco para a ONG aumenta se ela incorporar scripts, iframes, widgets, pixels ou redirecionamentos controlados por terceiros. A integração recomendada é somente um link.

Nenhum controle garante risco zero. A liberação exige testes, monitoramento, resposta a incidentes e revisão periódica.

## 2. Estado verificado do repositório

Na revisão de 10/11/2026, o repositório contém um servidor Python MCP executado por transporte `stdio`, conectores para APIs públicas com hosts fixos e catálogo local. Não foi identificado neste repositório um frontend web, aplicação HTTP pública, configuração de hospedagem web ou configuração de cabeçalhos HTTP. Portanto, controles de navegador, WAF, CDN, TLS e cabeçalhos devem ser aplicados no projeto/host que efetivamente servir o site público; não podem ser considerados ativos apenas por constarem neste documento.

O servidor MCP `stdio` não deve ser exposto diretamente à internet. Qualquer futuro transporte HTTP exige revisão própria, autenticação/autorização apropriadas ao caso, TLS, limites de requisição, isolamento e testes antes da publicação.

## 3. Integração segura para ONGs

### Integração permitida (recomendada)

- Link HTTPS simples para o domínio oficial, aberto em navegação normal.
- Texto e imagem estáticos hospedados pela própria ONG, sem JavaScript de terceiros.
- Identificação clara de que o Elas Conectadas é um serviço externo e independente.

Exemplo de link:

```html
<a href="https://DOMINIO-OFICIAL-A-CONFIRMAR/"
   target="_blank"
   rel="noopener noreferrer">
  Acesse o Elas Conectadas
</a>
```

O domínio acima é um marcador e não deve ser publicado até que o domínio oficial seja confirmado.

### Integrações não permitidas por padrão

- Não pedir à ONG para inserir script, tag de rastreamento, pixel, extensão ou código remoto do Elas Conectadas.
- Não recomendar iframe, proxy reverso ou espelhamento da aplicação.
- Não solicitar credenciais, tokens, acesso ao CMS, hospedagem, DNS ou banco de dados da ONG.
- Não usar redirecionador aberto (parâmetro de URL que aceite qualquer destino).
- Não carregar scripts, fontes, imagens ou bibliotecas de domínios desconhecidos.
- Não enviar dados de navegação, localização, necessidade de atendimento ou texto digitado da usuária para a ONG.

Se futuramente houver widget oficial, ele será um produto separado, com origem e recursos mínimos, sandbox, CSP, revisão de privacidade e teste independente. Não reutilizar a aplicação inteira em iframe.

## 4. Arquitetura em camadas para o site público

Os controles abaixo são requisitos para a aplicação web e a infraestrutura de hospedagem. Ainda não estão comprovados como implantados neste repositório.

### Borda, DNS e transporte

- HTTPS obrigatório; redirecionar HTTP para HTTPS.
- TLS moderno gerenciado pelo provedor; renovar certificados automaticamente.
- CDN/WAF com proteção contra abuso, bots e ataques volumétricos, respeitando limites do plano do provedor.
- Rate limiting por rota, com limites mais estritos para endpoints caros; limites e respostas 429 documentados.
- Não expor portas administrativas, banco de dados, painel de deploy ou servidor MCP diretamente à internet.
- Separar produção, preview e desenvolvimento; dados reais somente em produção com controles adequados.
- Restringir origens e destinos de rede; nunca aceitar URL arbitrária fornecida pela usuária para o servidor buscar (proteção contra SSRF).

### Cabeçalhos e política do navegador

Configurar no host web, depois de confirmar todas as origens legítimas utilizadas:

- `Strict-Transport-Security` com `includeSubDomains` somente após confirmar que todos os subdomínios suportam HTTPS.
- `Content-Security-Policy` restritiva, sem `unsafe-eval`; evitar `unsafe-inline` e usar nonce/hash quando necessário. Começar com `Content-Security-Policy-Report-Only` para mapear dependências legítimas antes de bloquear.
- `X-Content-Type-Options: nosniff`.
- `Referrer-Policy: strict-origin-when-cross-origin` ou mais restritiva.
- `Permissions-Policy` desabilitando câmera, microfone e geolocalização por padrão; habilitar geolocalização apenas por ação explícita e no contexto necessário.
- `frame-ancestors 'none'` se o produto não precisar ser incorporado. Se houver widget aprovado, usar allowlist específica e revisar clickjacking.
- `frame-ancestors` deve ser configurado em CSP; não confiar somente em X-Frame-Options para esse controle.
- Não liberar CORS com `*` quando houver credenciais. CORS deve permitir somente origens necessárias e nunca ser tratado como autenticação.

### Aplicação e APIs

- Validar tipos, tamanhos, formatos e limites de todos os parâmetros no servidor.
- Usar consultas parametrizadas; nunca concatenar entrada do usuário em SQL, shell, caminhos ou consultas.
- Codificar saída conforme o contexto HTML/JavaScript/URL para prevenir XSS.
- Evitar HTML arbitrário e Markdown não sanitizado vindo de catálogo, APIs ou modelos.
- Se houver redirecionamento, aceitar apenas destinos de uma allowlist HTTPS validada.
- Timeout, limite de tamanho de resposta, tratamento de erro e circuit breaker nas chamadas externas.
- Manter hosts de APIs externas em allowlist fixa; bloquear redirecionamentos para hosts não autorizados.
- Respostas de erro não devem expor stack trace, caminhos internos, variáveis de ambiente, tokens ou dados pessoais.
- Não armazenar segredos no código, frontend, repositório ou logs. Usar variáveis/secret manager do ambiente de execução e rotacionar credenciais expostas.
- Não usar dados reais de mulheres em testes, demos, prompts de depuração ou ambientes de preview.

### Privacidade e segurança de pessoas em situação de risco

- Não exigir cadastro, login, e-mail, senha ou CPF para consultas informativas.
- Minimizar localização: preferir município/UF; CEP opcional; localização precisa somente com consentimento explícito e justificativa.
- Não armazenar relatos de violência, dados de saúde, histórico de busca ou localização precisa por padrão.
- Não inserir texto livre da usuária em logs, analytics, rastreadores, ferramentas de terceiros ou relatórios de erro.
- Não revelar endereços sigilosos de abrigos nem dados de atendidas.
- Aplicar retenção mínima, acesso por necessidade, criptografia em trânsito e em repouso onde houver armazenamento.
- Informar claramente quando um CEP é enviado ao ViaCEP e quais dados são transmitidos a cada fonte externa.
- Não usar ferramentas de terceiros para rastrear usuárias em situação de vulnerabilidade.

## 5. Proteção do servidor MCP e conectores

- Manter o transporte `stdio` enquanto não houver necessidade validada de transporte remoto.
- Não executar ferramentas MCP com privilégios administrativos.
- Não aceitar comandos de shell, caminhos de arquivo ou URLs arbitrárias como argumentos de ferramentas.
- Manter conectores com hosts fixos e validação estrita de parâmetros.
- Usar timeouts curtos, limites de paginação e tratamento uniforme de erros.
- Evitar devolver campos pessoais ou desnecessários recebidos de fontes externas; normalizar e minimizar respostas.
- Não incluir conteúdo externo em instruções privilegiadas de sistema. Tratar texto retornado por sites e catálogos como dado não confiável, prevenindo prompt injection.
- Se uma API remota MCP for criada, exigir autenticação e autorização no gateway, TLS, rate limit, validação de origem quando aplicável, proteção contra replay/CSRF conforme o mecanismo de sessão e isolamento do processo.

## 6. Segurança da cadeia de desenvolvimento

Controles já presentes na pipeline na revisão: pytest, Ruff, Bandit, pip-audit, Gitleaks e Dependabot para dependências Python e GitHub Actions.

Controles adicionais propostos:
- CodeQL para análise estática contínua do código Python.
- Revisão humana de mudanças em autenticação, rede, dados, CORS, CSP, logging e implantação.
- Dependências atualizadas e vulnerabilidades críticas/altas corrigidas antes da publicação.
- Actions de terceiros revisadas e, em ambientes de produção maduros, fixadas por SHA imutável.
- Proteção da branch principal, revisão obrigatória, bloqueio de force-push e exigência de checks verdes.
- Segredos de produção separados de preview; permissões mínimas para tokens de CI.
- Gerar SBOM e registrar versões dos componentes no processo de release.

## 7. Modelo de ameaças resumido

| Ameaça | Consequência possível | Controle principal |
|---|---|---|
| XSS no site | Execução de código no navegador da usuária | CSP, escaping, sanitização e testes |
| Clickjacking | Interface enganosa sobreposta | CSP frame-ancestors e ausência de iframe |
| SSRF | Servidor acessa rede interna ou destinos indevidos | Hosts fixos, allowlist e sem URL arbitrária |
| Abuso/DoS | Indisponibilidade e custo elevado | CDN/WAF, rate limit, limites e timeouts |
| Dependência comprometida | Código malicioso na aplicação | Dependabot, pip-audit, CodeQL, revisão e SBOM |
| Segredo exposto | Acesso indevido a serviços | Secret manager, Gitleaks, rotação e privilégio mínimo |
| Prompt injection | Ferramenta/LLM segue instruções maliciosas de fonte externa | Separar dados de instruções e limitar ferramentas |
| Vazamento de dados sensíveis | Risco físico, social ou de privacidade | Minimização, não retenção, controle de acesso e revisão de logs |
| Link adulterado ou domínio falso | Phishing em nome do projeto | Domínio oficial estável, HTTPS e material de divulgação verificável |

## 8. Critérios obrigatórios antes de uma ONG divulgar o link

- [ ] Domínio oficial confirmado, HTTPS ativo e sem alerta de certificado.
- [ ] Aplicação web identificada e implantação de produção funcionando.
- [ ] CSP e cabeçalhos revisados em produção.
- [ ] WAF/CDN e rate limit configurados e testados.
- [ ] Nenhum segredo no bundle frontend, repositório público ou logs.
- [ ] Testes automatizados e scans sem achados críticos/altos não tratados.
- [ ] Testes de XSS, CSRF (se houver sessão), clickjacking, SSRF, open redirect, controle de acesso e abuso de API.
- [ ] Links externos e conteúdo de fontes não confiáveis tratados com segurança.
- [ ] Política de privacidade, retenção, canal de vulnerabilidade e plano de resposta a incidentes publicados.
- [ ] Teste independente de segurança (pentest) no ambiente autorizado antes de declarar o site pronto para parceria.

## 9. Resposta a incidentes

1. Suspender ou limitar a rota/versão afetada sem apagar evidências.
2. Preservar logs técnicos minimizados, sem divulgar dados pessoais.
3. Revogar e rotacionar segredos potencialmente expostos.
4. Corrigir a causa, executar testes de regressão e revisar o escopo do incidente.
5. Comunicar as instituições parceiras e pessoas afetadas quando aplicável, com orientação clara.
6. Reabrir o serviço somente após validação técnica e registro da decisão.

## 10. Declaração de transparência

A existência deste documento não significa que todos os controles estejam implementados. O status deve ser comprovado por configuração implantada, resultados de teste e revisão periódica. Não anunciar “100% seguro”, “impossível de invadir” ou “risco zero”.
