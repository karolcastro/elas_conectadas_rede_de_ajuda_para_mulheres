from elas_conectadas_mcp.services.menstrual_dignity import MenstrualDignityGuide

def test_guidance_includes_official_sources_and_access_note():
    result = MenstrualDignityGuide().get_guidance()
    assert result["program_name"] == "Programa Dignidade Menstrual"
    assert len(result["official_sources"]) == 3
    assert "não exige cadastro" in result["important_access_note"]
    assert "estoque" in result["availability_notice"]
