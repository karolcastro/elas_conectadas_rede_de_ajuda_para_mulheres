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



def test_sp_guide_exposes_verified_free_phone_and_scheduling_conditions():
    result = FreeLegalAidDirectory().guide(uf="sp", municipality="São Paulo")
    contact = result["state_specific_contacts"][0]
    assert contact["phone"] == "0800 773 4340"
    assert contact["free"] is True
    assert contact["appointment_required"] is True
    assert contact["documents_required_to_request"] is False
    assert contact["source_last_updated"] == "2026-09-09"
    assert result["state_specific_contacts"][1]["phone"] is None


def test_non_sp_guide_does_not_show_sp_specific_phone():
    result = FreeLegalAidDirectory().guide(uf="RJ")
    assert result["state_specific_contacts"] == []
