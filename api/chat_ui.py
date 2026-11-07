"""Experimental multi-provider chat UI backed by read-only MCP tools."""
from __future__ import annotations
import os, json, logging, asyncio
import httpx
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

MODEL = "gemini-3.8-flash"
logger = logging.getLogger("elas_conectadas.chat")
ALLOWED = {
 "consultar_telefones_de_urgencia","listar_canais_oficiais_de_ajuda",
 "buscar_servicos_protecao_por_localidade","orientar_consulta_rede_oficial_atendimento",
 "buscar_cursos_programas_para_mulheres","orientar_assistencia_juridica_gratuita",
 "orientar_acesso_creas","orientar_acesso_cras","orientar_acesso_moradia_popular",
 "orientar_acesso_alimentacao_gratuita","buscar_unidades_saude_por_municipio",
 "buscar_unidades_saude_por_cep","consultar_programa_dignidade_menstrual",
 "orientar_privacidade_e_seguranca"
}
SYSTEM = """Você é o Elas Conectadas, agente de apoio a mulheres no Brasil. Na primeira resposta, informe perigo imediato: Polícia Militar 190; orientação sobre violência contra a mulher: Ligue 180, gratuito e 24 horas. Pergunte o idioma preferido e siga em português até escolha. Acolha sem julgamento. Nunca exija cadastro, login, e-mail, senha, CPF ou relato detalhado. Peça somente município/UF quando suficiente; CEP é opcional. Use ferramentas para consultar fontes. Nunca invente serviço, contato, endereço, horário, vaga, gratuidade ou disponibilidade. Priorize gratuidade confirmada; custo desconhecido não é gratuito. Nunca divulgue endereços sigilosos de abrigos; encaminhe pelo 180. CNES/DEMAS é cadastro e não confirma agenda, gratuidade ou exame. Informe limites, fonte e data quando disponíveis."""
PAGE = """<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elas Conectadas</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f3fa;color:#2e263b;font:16px system-ui}header{background:#563b83;color:white;text-align:center;padding:22px}main{max-width:780px;margin:22px auto;padding:0 14px}.alert,.box{background:white;border-radius:14px;padding:17px;box-shadow:0 5px 22px #24143a14}.alert{border-left:5px solid #b84c70}.alert p{margin:6px 0}.alert a{color:#563b83;font-weight:700}.box{margin-top:15px}#msgs{height:48vh;overflow:auto;display:flex;flex-direction:column;gap:10px}.msg{padding:12px 14px;border-radius:13px;white-space:pre-wrap;max-width:90%;line-height:1.5}.bot{background:#f0ebf8;align-self:flex-start}.user{background:#563b83;color:white;align-self:flex-end}form{display:flex;gap:8px;margin-top:12px}textarea{flex:1;min-height:52px;padding:12px;border:1px solid #d7cee3;border-radius:10px;font:inherit}button{background:#563b83;color:white;border:0;border-radius:10px;padding:0 20px;font-weight:700}button:disabled{opacity:.5}.small{font-size:13px;line-height:1.5;color:#625b6d}@media(max-width:520px){form{flex-direction:column}button{height:46px}}</style>
<header><h1>Elas Conectadas</h1><p>Informação confiável, acolhimento e caminhos de apoio.</p></header><main>
<div class="alert"><b>Se precisar de ajuda agora</b><p>Perigo imediato: <a href="tel:190">Polícia Militar — 190</a>.</p><p>Orientação sobre violência contra a mulher: <a href="tel:180">Ligue 180</a> — gratuito, 24 horas.</p></div>
<div class="box"><div id="msgs" aria-live="polite"><div class="msg bot">Olá! Qual idioma você prefere? Posso continuar em português. Não é necessário cadastro. Para buscar apoio próximo, informe apenas município e estado; CEP é opcional. Evite compartilhar dados pessoais ou relatos detalhados.</div></div><form id="f"><textarea id="m" maxlength="2000" placeholder="Como posso ajudar?"></textarea><button id="s">Enviar</button></form><p class="small">Este agente facilita o acesso à informação e não substitui emergência ou profissionais. Não informe CPF, senhas ou detalhes que identifiquem você. Confirme diretamente com o serviço os dados de atendimento.</p></div></main>
<script>
const f=document.querySelector('#f'),m=document.querySelector('#m'),s=document.querySelector('#s'),msgs=document.querySelector('#msgs'),history=[];
function add(t,c){let d=document.createElement('div');d.className='msg '+c;d.textContent=t;msgs.append(d);msgs.scrollTop=msgs.scrollHeight}
f.onsubmit=async e=>{e.preventDefault();let text=m.value.trim();if(!text||s.disabled)return;add(text,'user');m.value='';s.disabled=true;s.textContent='Aguarde…';try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text,history})});let d=await r.json();if(!r.ok)throw Error(d.error||'Não foi possível responder.');add(d.reply,'bot');history.push({role:'user',text},{role:'model',text:d.reply});while(history.length>8)history.shift()}catch(e){add(e.message,'bot')}finally{s.disabled=false;s.textContent='Enviar'}};
m.onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();f.requestSubmit()}};
</script></html>"""

def _text_result(result):
    content=getattr(result,"content",None) or []
    return "\n".join(getattr(x,"text",str(x)) for x in content)[:10000] or json.dumps(getattr(result,"structuredContent",{}),ensure_ascii=False)[:10000]


def _gemini_schema(schema):
    """Convert Pydantic/MCP JSON Schema to Gemini's supported subset."""
    if isinstance(schema, list):
        return [_gemini_schema(item) for item in schema]
    if not isinstance(schema, dict):
        return schema
    if "anyOf" in schema:
        options = [item for item in schema["anyOf"] if isinstance(item, dict) and item.get("type") != "null"]
        if len(options) == 1:
            merged = dict(options[0])
            for key in ("description",):
                if key in schema and key not in merged:
                    merged[key] = schema[key]
            return _gemini_schema(merged)
    allowed = {"type", "description", "enum", "items", "properties", "required", "format"}
    normalized = {
        key: _gemini_schema(value)
        for key, value in schema.items()
        if key in allowed and value is not None
    }
    # Gemini valida cada item de "required" contra as chaves de "properties".
    # MCP/Pydantic pode emitir required junto de schemas com allOf/$ref ou
    # propriedades que foram removidas na conversão; nunca encaminhe nomes órfãos.
    properties = normalized.get("properties")
    required = normalized.get("required")
    if required is not None:
        if isinstance(properties, dict):
            normalized["required"] = [name for name in required if name in properties]
        else:
            normalized.pop("required", None)
    return normalized

class ProviderUnavailable(Exception):
    def __init__(self, provider, status=None, reason="unavailable"):
        self.provider = provider
        self.status = status
        self.reason = reason
        super().__init__(f"{provider}:{reason}:{status}")


def _openai_tools(declarations):
    """Convert MCP declarations to OpenAI Chat Completions function tools."""
    return [
        {
            "type": "function",
            "function": {
                "name": item["name"],
                "description": item.get("description", item["name"]),
                "parameters": item.get("parameters") or {"type": "object", "properties": {}},
            },
        }
        for item in declarations
    ]


async def _execute_tool_calls(mcp, calls, provider):
    results = []
    for call in calls:
        name = call.get("name", "")
        if name not in ALLOWED:
            result = "Ferramenta não permitida."
        else:
            try:
                args = call.get("args") if provider == "gemini" else call.get("arguments")
                if isinstance(args, str):
                    args = json.loads(args or "{}")
                if not isinstance(args, dict):
                    args = {}
                result = _text_result(await mcp.call_tool(name, args))
            except Exception:
                logger.exception("MCP tool call failed provider=%s tool=%s", provider, name)
                result = "Consulta indisponível. Não invente resultados."
        results.append((call, result))
    return results


async def _run_gemini(client, key, contents, declarations, mcp):
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM}]},
        "contents": list(contents),
        "tools": [{"functionDeclarations": declarations}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1200},
    }
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    retried_503 = False
    for _ in range(5):
        try:
            response = await client.post(
                endpoint, headers={"x-goog-api-key": key}, json=body
            )
        except httpx.TimeoutException as exc:
            logger.warning("Gemini request timed out; retrying once")
            try:
                response = await client.post(
                    endpoint, headers={"x-goog-api-key": key}, json=body
                )
            except httpx.TimeoutException as retry_exc:
                raise ProviderUnavailable("gemini", reason="timeout") from retry_exc
        if response.status_code == 503 and not retried_503:
            retried_503 = True
            logger.warning("Gemini returned HTTP 503; retrying once")
            await asyncio.sleep(1.5)
            continue
        if response.status_code == 429 or response.status_code >= 500:
            raise ProviderUnavailable("gemini", response.status_code)
        if response.status_code >= 400:
            logger.error("Gemini API rejected request status=%s body=%s", response.status_code, response.text[:1000])
            raise RuntimeError(f"Gemini recusou a solicitação (HTTP {response.status_code}).")
        candidates = response.json().get("candidates") or []
        if not candidates:
            raise RuntimeError("O Gemini não retornou uma resposta.")
        candidate = candidates[0].get("content", {})
        parts = candidate.get("parts", [])
        calls = [
            {"name": part["functionCall"].get("name", ""), "args": part["functionCall"].get("args") or {}}
            for part in parts if "functionCall" in part
        ]
        if not calls:
            answer = "\n".join(part.get("text", "") for part in parts if part.get("text")).strip()
            return answer or "Não consegui responder. Pode reformular?"
        body["contents"].append(candidate)
        results = await _execute_tool_calls(mcp, calls, "gemini")
        for call, result in results:
            body["contents"].append({
                "role": "function",
                "parts": [{
                    "functionResponse": {
                        "name": call["name"],
                        "response": {"result": result},
                    }
                }],
            })
    raise RuntimeError("A consulta excedeu o limite de etapas. Tente ser mais específica.")


async def _run_openai(client, key, messages, tools, mcp):
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    request_messages = list(messages)
    endpoint = "https://api.openai.com/v1/chat/completions"
    for _ in range(5):
        try:
            response = await client.post(
                endpoint,
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": model,
                    "messages": request_messages,
                    "tools": tools,
                    "tool_choice": "auto",
                    "temperature": 0.2,
                    "max_completion_tokens": 1200,
                    "store": False,
                },
            )
        except httpx.TimeoutException as exc:
            logger.warning("OpenAI request timed out")
            raise ProviderUnavailable("openai", reason="timeout") from exc
        if response.status_code == 429 or response.status_code >= 500:
            raise ProviderUnavailable("openai", response.status_code)
        if response.status_code >= 400:
            logger.error("OpenAI API rejected request status=%s body=%s", response.status_code, response.text[:1000])
            raise RuntimeError(f"A OpenAI recusou a solicitação (HTTP {response.status_code}).")
        choices = response.json().get("choices") or []
        if not choices:
            raise RuntimeError("A OpenAI não retornou uma resposta.")
        message = choices[0].get("message") or {}
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            return str(message.get("content") or "").strip() or "Não consegui responder. Pode reformular?"
        request_messages.append(message)
        calls = []
        for item in tool_calls:
            function = item.get("function") or {}
            calls.append({
                "id": item.get("id", ""),
                "name": function.get("name", ""),
                "arguments": function.get("arguments", "{}"),
            })
        results = await _execute_tool_calls(mcp, calls, "openai")
        for call, result in results:
            request_messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": str(result),
            })
    raise RuntimeError("A consulta excedeu o limite de etapas. Tente ser mais específica.")


def register_chat_routes(mcp):
    @mcp.custom_route("/", methods=["GET"])
    async def home(request: Request):
        return HTMLResponse(PAGE)

    @mcp.custom_route("/chat", methods=["POST"])
    async def chat(request: Request):
        try:
            data = await request.json()
            message = str(data.get("message", "")).strip()
            if not message or len(message) > 2000:
                return JSONResponse({"error": "Envie uma mensagem de até 2.000 caracteres."}, status_code=400)

            gemini_key = os.getenv("GEMINI_API_KEY")
            openai_key = os.getenv("OPENAI_API_KEY")
            if not gemini_key and not openai_key:
                return JSONResponse({"error": "O serviço de conversa não está configurado."}, status_code=503)

            history = data.get("history", [])
            history = history[-8:] if isinstance(history, list) else []
            contents = []
            openai_messages = [{"role": "system", "content": SYSTEM}]
            for item in history:
                if not isinstance(item, dict) or item.get("role") not in ("user", "model") or not item.get("text"):
                    continue
                text = str(item["text"])[:2000]
                gemini_role = item["role"]
                contents.append({"role": gemini_role, "parts": [{"text": text}]})
                openai_messages.append({
                    "role": "assistant" if gemini_role == "model" else "user",
                    "content": text,
                })
            contents.append({"role": "user", "parts": [{"text": message}]})
            openai_messages.append({"role": "user", "content": message})

            declarations = []
            for tool in await mcp.list_tools():
                if tool.name in ALLOWED:
                    declarations.append({
                        "name": tool.name,
                        "description": (tool.description or tool.name)[:800],
                        "parameters": _gemini_schema(tool.inputSchema),
                    })
            openai_tools = _openai_tools(declarations)

            # Gemini permanece como principal. OpenAI só é acionada se houver
            # indisponibilidade transitória, limite de uso ou timeout no Gemini.
            async with httpx.AsyncClient(timeout=httpx.Timeout(20.0, connect=8.0)) as client:
                if gemini_key:
                    try:
                        answer = await _run_gemini(client, gemini_key, contents, declarations, mcp)
                        return JSONResponse({"reply": answer, "provider": "gemini"})
                    except ProviderUnavailable as exc:
                        logger.warning(
                            "Primary provider unavailable provider=%s status=%s reason=%s; trying fallback",
                            exc.provider, exc.status, exc.reason,
                        )
                        if not openai_key:
                            return JSONResponse({
                                "error": "O Gemini está temporariamente indisponível e não há um provedor alternativo configurado. Tente novamente em alguns instantes."
                            }, status_code=503)
                if openai_key:
                    try:
                        answer = await _run_openai(client, openai_key, openai_messages, openai_tools, mcp)
                        return JSONResponse({"reply": answer, "provider": "openai"})
                    except ProviderUnavailable as exc:
                        logger.error(
                            "Fallback provider unavailable provider=%s status=%s reason=%s",
                            exc.provider, exc.status, exc.reason,
                        )
                        return JSONResponse({
                            "error": "Os serviços de IA estão temporariamente indisponíveis. Tente novamente em alguns instantes."
                        }, status_code=503)
            return JSONResponse({"error": "Não foi possível responder neste momento."}, status_code=503)
        except Exception:
            logger.exception("Unhandled error while processing /chat request")
            return JSONResponse({"error": "Erro ao processar a mensagem. Tente novamente."}, status_code=500)
