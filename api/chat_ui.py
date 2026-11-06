"""Experimental stateless Gemini chat UI backed by read-only MCP tools."""
from __future__ import annotations
import os, json, logging
import httpx
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

MODEL = "gemini-3.8-flash"
logger = logging.getLogger("elas_conectadas.gemini")
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
    return {key: _gemini_schema(value) for key, value in schema.items() if key in allowed and value is not None}

def _gemini_error(status, response_text):
    """Return a safe user-facing diagnosis without exposing credentials."""
    try:
        payload = json.loads(response_text)
        detail = payload.get("error", {}).get("message", "")
    except Exception:
        detail = ""
    detail = str(detail)[:350]
    if status in (401, 403):
        return "O Google recusou a credencial ou a permissão da API (HTTP %s). Confira se GEMINI_API_KEY é uma chave válida do Gemini API e se a API está habilitada no projeto Google." % status
    if status == 404:
        return "O modelo ou endpoint não foi encontrado (HTTP 404). O identificador configurado é %s." % MODEL
    if status == 429:
        return "A cota ou limite de uso do Gemini foi atingido (HTTP 429). Verifique os limites do projeto Google."
    if status == 400:
        return "O Gemini rejeitou o formato da solicitação (HTTP 400). Os parâmetros das ferramentas podem ser incompatíveis. Detalhe: %s" % (detail or "sem detalhe fornecido")
    return "O Gemini retornou HTTP %s. %s" % (status, detail or "Tente novamente mais tarde.")

def register_chat_routes(mcp):
    @mcp.custom_route("/", methods=["GET"])
    async def home(request: Request):
        return HTMLResponse(PAGE)
    @mcp.custom_route("/chat", methods=["POST"])
    async def chat(request: Request):
        key=os.getenv("GEMINI_API_KEY")
        if not key:return JSONResponse({"error":"O serviço de conversa não está configurado."},status_code=503)
        try:
            data=await request.json(); message=str(data.get("message","")).strip()
            if not message or len(message)>2000:return JSONResponse({"error":"Envie uma mensagem de até 2.000 caracteres."},status_code=400)
            history=data.get("history",[]); history=history[-8:] if isinstance(history,list) else []
            contents=[]
            for h in history:
                if isinstance(h,dict) and h.get("role") in ("user","model") and h.get("text"):
                    contents.append({"role":h["role"],"parts":[{"text":str(h["text"])[:2000]}]})
            contents.append({"role":"user","parts":[{"text":message}]})
            declarations=[]
            for t in await mcp.list_tools():
                if t.name in ALLOWED:declarations.append({"name":t.name,"description":(t.description or t.name)[:800],"parameters":_gemini_schema(t.inputSchema)})
            body={"systemInstruction":{"parts":[{"text":SYSTEM}]},"contents":contents,"tools":[{"functionDeclarations":declarations}],"generationConfig":{"temperature":0.2,"maxOutputTokens":1200}}
            endpoint=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
            async with httpx.AsyncClient(timeout=45) as client:
                for _ in range(5):
                    r=await client.post(endpoint,headers={"x-goog-api-key":key},json=body)
                    if r.status_code>=400:
                        logger.error("Gemini API error status=%s body=%s", r.status_code, r.text[:1200])
                        return JSONResponse({"error":_gemini_error(r.status_code, r.text)},status_code=502)
                    candidates=r.json().get("candidates") or []
                    if not candidates:return JSONResponse({"error":"A IA não retornou resposta."},status_code=502)
                    c=candidates[0].get("content",{}); parts=c.get("parts",[])
                    calls=[p["functionCall"] for p in parts if "functionCall" in p]
                    if not calls:
                        answer="\n".join(p.get("text","") for p in parts if p.get("text")).strip()
                        return JSONResponse({"reply":answer or "Não consegui responder. Pode reformular?"})
                    body["contents"].append(c)
                    for call in calls:
                        name=call.get("name","")
                        if name not in ALLOWED:result="Ferramenta não permitida."
                        else:
                            try:result=_text_result(await mcp.call_tool(name,call.get("args") or {}))
                            except Exception:result="Consulta indisponível. Não invente resultados."
                        body["contents"].append({"role":"function","parts":[{"functionResponse":{"name":name,"response":{"result":result}}}]})
            return JSONResponse({"error":"A consulta excedeu o limite de etapas. Tente ser mais específica."},status_code=502)
        except Exception:
            return JSONResponse({"error":"Erro ao processar a mensagem. Tente novamente."},status_code=500)
