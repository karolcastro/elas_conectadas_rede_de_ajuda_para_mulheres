import pytest

from elas_conectadas_mcp.services.women_organizations import WomenOrganizationsGuide


def test_guide_returns_discovery_sources_and_curated_free_initiatives():
    result = WomenOrganizationsGuide().guide(uf="SP", municipality="São Paulo")
    assert result["requested_location"]["uf"] == "SP"
    assert result["automated_organization_results"] is False
    assert any("IPEA" in item["name"] for item in result["discovery_sources"])
    assert any("Ligue 180" in item["name"] for item in result["discovery_sources"])
    assert any("gratuitamente" in item for item in result["validation_checklist"])

    initiatives = {item["name"]: item for item in result["verified_organizations"]}
    assert initiatives["TamoJuntas"]["cost"] == "Gratuito, conforme declaração institucional."
    assert initiatives["TamoJuntas"]["state_contact"] == "tamojuntas.sp@tamojuntas.org.br"
    assert initiatives["Mapa do Acolhimento"]["cost"].startswith("Gratuito")
    assert "formulário externo" in initiatives["Mapa do Acolhimento"]["limitations"]


def test_tamojuntas_state_contact_is_not_misrepresented_as_national_contact():
    result = WomenOrganizationsGuide().guide(uf="PE")
    tamojuntas = next(
        item for item in result["verified_organizations"] if item["name"] == "TamoJuntas"
    )
    assert tamojuntas["state_contact"] == "tamojuntas.pe@tamojuntas.org.br"
    assert "contato imediato" in tamojuntas["limitations"] or "atendimento imediato" in tamojuntas["limitations"]


def test_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        WomenOrganizationsGuide().guide(uf="São Paulo")


def test_guide_rejects_short_municipality():
    with pytest.raises(ValueError, match="município"):
        WomenOrganizationsGuide().guide(municipality="X")
