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


def test_bahia_guide_exposes_official_disque_defensoria_channels():
    result = FreeLegalAidDirectory().guide(uf="BA")
    contact = result["state_specific_contacts"][0]
    assert contact["phone"] == "129 ou 0800 071 3121"
    assert contact["free"] is True
    assert contact["source_last_updated"] == "2026-07-17"
    assert "ba.gov.br" in contact["official_source"]


def test_parana_guide_exposes_nudem_contact_and_scheduling():
    result = FreeLegalAidDirectory().guide(uf="PR")
    general, nudem = result["state_specific_contacts"]
    assert general["phone"] == "(41) 99123-1961"
    assert general["free"] is True
    assert "independentemente de renda" in general["audience"]
    assert nudem["phone"] == "(41) 99285-8134"
    assert nudem["email"] == "nudem@defensoria.pr.def.br"
    assert nudem["appointment_required"] is True
    assert nudem["source_last_updated"] == "2026-09-29"


def test_state_specific_contacts_do_not_leak_between_states():
    for uf in ("RJ", "AC", "GO"):
        result = FreeLegalAidDirectory().guide(uf=uf)
        assert result["state_specific_contacts"] == []
    assert FreeLegalAidDirectory().guide(uf="MG")["state_specific_contacts"][0]["phone"].startswith("(31)")
    assert FreeLegalAidDirectory().guide(uf="PE")["state_specific_contacts"][0]["phone"] == "(81) 99488-3765"


def test_minas_gerais_guide_exposes_nudem_bh_with_local_scope():
    result = FreeLegalAidDirectory().guide(uf="MG")
    contact = result["state_specific_contacts"][0]
    assert contact["phone"] == "(31) 98475-2616 / (31) 98239-8863"
    assert contact["service_hours"] == "Segunda a sexta-feira, das 11h às 17h."
    assert "Belo Horizonte" in contact["name"]
    assert contact["free"] is True


def test_pernambuco_guide_exposes_nudem_whatsapp_and_message_only_notice():
    result = FreeLegalAidDirectory().guide(uf="PE")
    contact = result["state_specific_contacts"][0]
    assert contact["phone"] == "(81) 99488-3765"
    assert contact["service_modes"] == ["WhatsApp por mensagem"]
    assert contact["source_last_updated"] == "2026-09-25"
    assert "ordem de chegada" in contact["important_notice"]


def test_legal_aid_guide_includes_official_free_creas_locator():
    result = FreeLegalAidDirectory().guide(uf="AC")
    creas = next(x for x in result["official_directories"] if x["name"].endswith("CREAS"))
    assert creas["source_last_updated"] == "2026-10-26"
    assert "gov.br/mds" in creas["url"]


def test_creas_guide_is_free_and_points_to_official_mds_locator():
    result = FreeLegalAidDirectory().creas_guide(uf="PE", municipality="Recife")
    assert result["free"] is True
    assert result["public_service"] is True
    assert result["requested_location"] == {"uf": "PE", "municipality": "Recife"}
    assert "aplicacoes.mds.gov.br" in result["official_locator"]
    assert result["source_last_updated"] == "2026-10-26"
    assert "psicológica" in result["audience"]


def test_creas_guide_rejects_invalid_location():
    with pytest.raises(ValueError, match="UF"):
        FreeLegalAidDirectory().creas_guide(uf="Pernambuco")


def test_cras_guide_explains_free_social_protection_and_cadunico_access():
    result = FreeLegalAidDirectory().cras_guide(uf="SP", municipality="São Paulo")
    assert result["free"] is True
    assert result["public_service"] is True
    assert result["requested_location"]["uf"] == "SP"
    assert any("Cadastro Único" in item for item in result["services"])
    assert "não garante concessão automática" in result["how_to_access"][-2]
    assert "gov.br" in result["official_source"]
    assert "Não envie CPF" in result["limitations"][-1]


def test_cras_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        FreeLegalAidDirectory().cras_guide(uf="São Paulo")



def test_cras_guide_includes_municipal_emergency_benefits_for_food_and_housing():
    result = FreeLegalAidDirectory().cras_guide(uf="SP", municipality="São Paulo")
    assert "beneficios_eventuais_source" in result
    assert any("Benefícios Eventuais" in item for item in result["services"])
    assert any("falta de alimentos" in item for item in result["how_to_access"])
    assert "regulamentação local" in result["how_to_access"][-1]


def test_housing_guide_explains_women_priority_without_promising_free_housing():
    result = FreeLegalAidDirectory().housing_guide(uf="SP", municipality="São Paulo")
    assert result["public_program"] is True
    assert result["free"] is False
    assert any("mulher é responsável" in item for item in result["priority_groups"])
    assert any("vítimas de violência doméstica" in item for item in result["priority_groups"])
    assert any("não garante seleção" in item for item in result["limitations"])
    assert "Cadastro Único" in result["how_to_access"][0]


def test_housing_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        FreeLegalAidDirectory().housing_guide(uf="São Paulo")



def test_food_security_guide_prioritizes_free_meals_and_discloses_local_limits():
    result = FreeLegalAidDirectory().food_security_guide(uf="SP", municipality="São Paulo")
    assert result["requested_location"] == {"uf": "SP", "municipality": "São Paulo"}
    options = {item["name"]: item for item in result["options"]}
    assert options["Cozinhas Solidárias"]["free"] is True
    assert options["Cozinhas Comunitárias"]["free"] is None
    assert options["Restaurantes Populares"]["free"] is None
    assert result["automated_local_results"] is False
    assert any("nem confirma vagas" in item for item in result["limitations"])


def test_food_security_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        FreeLegalAidDirectory().food_security_guide(uf="São Paulo")


def test_vulnerable_women_guide_lists_official_benefits_and_free_services():
    result = FreeLegalAidDirectory().vulnerable_women_guide(uf="SP", municipality="São Paulo")
    assert result["requested_location"] == {"uf": "SP", "municipality": "São Paulo"}
    programs = {item["name"]: item for item in result["programs_and_services"]}
    assert programs["Cadastro Único (CadÚnico)"]["free_to_access"] is True
    assert programs["Bolsa Família — prioridade de atendimento às mulheres"]["free_to_access"] is True
    assert programs["Benefício de Prestação Continuada (BPC)"]["free_to_access"] is True
    assert programs["Centro POP"]["free_to_access"] is True
    assert result["automated_local_results"] is False
    assert any("sigilosos" in item for item in result["important_limits"])


def test_vulnerable_women_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        FreeLegalAidDirectory().vulnerable_women_guide(uf="São Paulo")

