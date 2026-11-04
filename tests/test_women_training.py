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
