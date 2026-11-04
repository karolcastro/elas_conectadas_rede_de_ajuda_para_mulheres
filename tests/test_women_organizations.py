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
    assert initiatives["Maria d'Ajuda — MariaLab"]["cost"].startswith("Gratuito")
    assert initiatives["Maria d'Ajuda — MariaLab"]["contact_email"] == "sos@mariadajuda.org"
    assert initiatives["Maria d'Ajuda — MariaLab"]["territorial_scope"].startswith("América Latina")
    pending = {item["name"]: item for item in result["organizations_requiring_cost_confirmation"]}
    assert pending["Marias da Internet"]["cost"].startswith("Não confirmado")
    safernet = result["scope_notes"][0]
    assert safernet["name"] == "SaferNet — Helpline"
    assert "adultos não são elegíveis" in safernet["note"]


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


def test_organizations_are_ranked_by_confirmed_local_presence_first():
    result = WomenOrganizationsGuide().guide(uf="SP", municipality="São Paulo")
    initiatives = {item["name"]: item for item in result["verified_organizations"]}
    assert initiatives["TamoJuntas"]["locality_match"] == "presential_city_published"
    assert initiatives["TamoJuntas"]["locality_priority"] == 0
    assert result["verified_organizations"][0]["name"] == "TamoJuntas"


def test_tamojuntas_does_not_claim_local_presence_in_other_city_of_same_state():
    result = WomenOrganizationsGuide().guide(uf="SP", municipality="Campinas")
    tamojuntas = next(
        item for item in result["verified_organizations"] if item["name"] == "TamoJuntas"
    )
    assert tamojuntas["locality_match"] == "state_contact_published_no_local_service_confirmation"
    assert "orientações e encaminhamentos" in tamojuntas["locality_evidence"]


def test_national_online_initiatives_are_distinguished_from_local_presence():
    result = WomenOrganizationsGuide().guide(uf="AM", municipality="Manaus")
    initiatives = {item["name"]: item for item in result["verified_organizations"]}
    assert initiatives["Mapa do Acolhimento"]["locality_match"] == "national_online_scope"
    assert initiatives["Maria d'Ajuda — MariaLab"]["locality_match"] == "latin_america_online_scope"
    assert initiatives["TamoJuntas"]["locality_match"] == "no_local_service_confirmation"


def test_city_matching_ignores_accents_and_case():
    result = WomenOrganizationsGuide().guide(uf="RJ", municipality="RIO DE JANEIRO")
    tamojuntas = next(
        item for item in result["verified_organizations"] if item["name"] == "TamoJuntas"
    )
    assert tamojuntas["locality_match"] == "presential_city_published"


def test_without_location_no_local_presence_is_assumed():
    result = WomenOrganizationsGuide().guide()
    tamojuntas = next(
        item for item in result["verified_organizations"] if item["name"] == "TamoJuntas"
    )
    assert tamojuntas["locality_match"] == "location_not_provided"



def test_new_national_free_support_programs_are_listed_with_access_limits():
    result = WomenOrganizationsGuide().guide(uf="SP", municipality="São Paulo")
    initiatives = {item["name"]: item for item in result["verified_organizations"]}

    acolhe = initiatives["Acolhe Mais — SUS"]
    assert acolhe["cost"].startswith("Gratuito")
    assert acolhe["territorial_scope"].startswith("Brasil")
    assert "conta gov.br" in acolhe["access_requirements"]
    assert "não solicita conta gov.br" in acolhe["limitations"]

    lbv = initiatives["Programa Ser Mulher — LBV"]
    assert lbv["cost"].startswith("Gratuito")
    assert "2022" in lbv["limitations"]
    assert lbv["contact_phone"] == "(11) 9999-66-557"


def test_numape_is_identified_as_parana_regional_network_not_national_service():
    result = WomenOrganizationsGuide().guide(uf="PR", municipality="Curitiba")
    numape = next(
        item for item in result["verified_organizations"]
        if item["name"] == "NUMAPE — Núcleo Maria da Penha"
    )
    assert numape["cost"].startswith("Gratuito")
    assert numape["locality_match"] == "statewide_regional_network"
    assert "não é atendimento automaticamente disponível em todos os municípios" in numape["territorial_scope"]

    outside = WomenOrganizationsGuide().guide(uf="SP", municipality="São Paulo")
    numape_outside = next(
        item for item in outside["verified_organizations"]
        if item["name"] == "NUMAPE — Núcleo Maria da Penha"
    )
    assert numape_outside["locality_match"] == "state_not_covered"
