import pytest

from elas_conectadas_mcp.services.women_organizations import WomenOrganizationsGuide


def test_guide_returns_discovery_sources_and_does_not_claim_verified_local_organizations():
    result = WomenOrganizationsGuide().guide(uf="SP", municipality="São Paulo")
    assert result["requested_location"]["uf"] == "SP"
    assert result["automated_organization_results"] is False
    assert any("IPEA" in item["name"] for item in result["discovery_sources"])
    assert any("Ligue 180" in item["name"] for item in result["discovery_sources"])
    assert any("gratuitamente" in item for item in result["validation_checklist"])


def test_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        WomenOrganizationsGuide().guide(uf="São Paulo")
