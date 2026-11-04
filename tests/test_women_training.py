import pytest

from elas_conectadas_mcp.services.women_training import WomenTrainingDirectory


def test_training_directory_returns_national_and_state_programs():
    result = WomenTrainingDirectory().search(uf="SP")
    ids = {item["id"] for item in result["programs"]}
    assert "sp-qualifica-ela-empreende" in ids
    assert "br-mds-educacao-financeira-mulheres" in ids
    assert all(item["free"] is True for item in result["programs"])
    assert all(item["official_source"].startswith("https://") for item in result["programs"])


def test_training_directory_filters_state_programs_and_keeps_national_programs():
    result = WomenTrainingDirectory().search(uf="MG")
    ids = {item["id"] for item in result["programs"]}
    assert "sp-qualifica-ela-empreende" not in ids
    assert "br-mds-educacao-financeira-mulheres" in ids
    assert "br-mec-mulheres-mil" in ids

    outside_offer = WomenTrainingDirectory().search(uf="RJ")
    outside_ids = {item["id"] for item in outside_offer["programs"]}
    assert "br-mec-mulheres-mil" not in outside_ids


def test_training_directory_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        WomenTrainingDirectory().search(uf="São Paulo")


def test_women_led_training_is_prioritized_and_identified():
    result = WomenTrainingDirectory().search()
    assert result["programs"][0]["provider"] == "WoMakersCode / Mais Mulheres em Tech"
    womakers = [
        item for item in result["programs"]
        if item["provider"] == "WoMakersCode / Mais Mulheres em Tech"
    ]
    assert len(womakers) == 3
    assert all(item["free"] is True for item in womakers)
    assert all(item["women_specific"] is True for item in womakers)
    assert all(item["verification_date"] == "2026-11-04" for item in womakers)


def test_women_led_national_courses_are_available_in_state_filter():
    result = WomenTrainingDirectory().search(uf="AM")
    ids = {item["id"] for item in result["programs"]}
    assert "br-womakerscode-introducao-ia" in ids
    assert "br-womakerscode-como-conseguir-emprego" in ids
    assert "br-womakerscode-lideranca-feminina" in ids
