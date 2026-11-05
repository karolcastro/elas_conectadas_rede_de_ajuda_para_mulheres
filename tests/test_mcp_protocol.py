"""End-to-end MCP protocol smoke tests over the original stdio transport."""

import json
import json
import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_stdio_mcp_lists_tools_and_runs_synthetic_women_queries() -> None:
    server = StdioServerParameters(
        command=sys.executable,
        args=["-c", "from elas_conectadas_mcp.server import main; main()"],
    )

    async with (
        stdio_client(server) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        initialized = await session.initialize()
        assert initialized.protocolVersion

        listed = await session.list_tools()
        tool_names = {tool.name for tool in listed.tools}

        assert "consultar_telefones_de_urgencia" in tool_names
        assert "buscar_servicos_protecao_por_localidade" in tool_names
        assert "buscar_cursos_programas_para_mulheres" in tool_names
        assert "buscar_iniciativas_mulheres_negras_indigenas" in tool_names

        emergency = await session.call_tool(
            "consultar_telefones_de_urgencia",
            arguments={},
        )
        assert emergency.isError is False
        emergency_text = "\\n".join(
            block.text for block in emergency.content if hasattr(block, "text")
        )
        assert "190" in emergency_text
        assert "180" in emergency_text

        protection = await session.call_tool(
            "buscar_servicos_protecao_por_localidade",
            arguments={"uf": "SP", "municipio": "São Paulo"},
        )
        assert protection.isError is False
        protection_text = "\\n".join(
            block.text for block in protection.content if hasattr(block, "text")
        )
        protection_data = json.loads(protection_text)
        assert isinstance(protection_data.get("services"), list)
        assert protection_data["filters"]["uf"] == "SP"
        assert protection_data["filters"]["municipality"] == "São Paulo"

        training = await session.call_tool(
            "buscar_cursos_programas_para_mulheres",
            arguments={"uf": "SP"},
        )
        assert training.isError is False
        training_text = "\\n".join(
            block.text for block in training.content if hasattr(block, "text")
        )
        training_data = json.loads(training_text)
        assert isinstance(training_data.get("programs"), list)
        assert training_data["filter"]["uf"] == "SP"

        initiatives = await session.call_tool(
            "buscar_iniciativas_mulheres_negras_indigenas",
            arguments={"uf": "AM", "publico": "indigenas", "tipo": "fortalecimento_coletivo"},
        )
        assert initiatives.isError is False
        initiatives_text = "\\n".join(
            block.text for block in initiatives.content if hasattr(block, "text")
        )
        initiatives_data = json.loads(initiatives_text)
        initiative_ids = {item["id"] for item in initiatives_data["opportunities"]}
        assert "br-fas-parentas-que-fazem" in initiative_ids
        assert "br-anmiga-mapa-articulacao-mulheres-indigenas" in initiative_ids
