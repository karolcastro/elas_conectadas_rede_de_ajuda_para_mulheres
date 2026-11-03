import pytest

from elas_conectadas_mcp.services.free_legal_aid import FreeLegalAidDirectory


def test_guide_returns_official_directories_without_claiming_local_results():
    result = FreeLegalAidDirectory().guide(uf="SP", municipality="São Paulo")
    assert result["requested_location"]["uf"] == "SP"
    assert result["automated_local_results"] is False
    assert any(item["name"].startswith("Conselho Nacional de Justiça") for item in result["official_directories"])
    assert any(item["name"] == "Ligue 180" for item in result["official_directories"])


def test_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        FreeLegalAidDirectory().guide(uf="São Paulo")


def test_guide_rejects_short_municipality():
    with pytest.raises(ValueError, match="município"):
        FreeLegalAidDirectory().guide(municipality="X")
