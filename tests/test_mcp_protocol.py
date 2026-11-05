"""End-to-end MCP protocol smoke test over the original stdio transport."""

import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_stdio_mcp_lists_tools_and_returns_official_helplines() -> None:
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

            result = await session.call_tool(
                "consultar_telefones_de_urgencia",
                arguments={},
            )

            assert result.isError is False
            response_text = "\n".join(
                block.text for block in result.content if hasattr(block, "text")
            )
            assert "190" in response_text
            assert "180" in response_text
