import pytest

from elas_conectadas_mcp.services.women_economic_autonomy import (
    WomenEconomicAutonomyDirectory,
)


def test_directory_prioritizes_current_indigenous_women_training():
    result = WomenEconomicAutonomyDirectory().search(publico="indigenas")
    recode = next(
        item for item in result["opportunities"]
        if item["id"] == "br-recode-comunicadoras-indigenas-2026"
    )
    assert recode["free"] is True
    assert recode["status"] == "inscricoes_abertas"
    assert "16 anos" in recode["audience"]


def test_directory_explains_restricted_seed_funding_for_black_women():
    result = WomenEconomicAutonomyDirectory().search(publico="negras")
    impact = next(
        item for item in result["opportunities"]
        if item["id"] == "br-irme-impacto-feminino-capital-semente-2026"
    )
    assert impact["status"] == "apoio_aberto_apenas_coorte"
    assert "exclusivamente para participantes" in impact["status_detail"]
    assert "R$ 1.000" in " ".join(impact["support"])


def test_directory_filters_by_state_and_collective_strengthening():
    result = WomenEconomicAutonomyDirectory().search(
        uf="AM", publico="indigenas", tipo="fortalecimento_coletivo"
    )
    ids = {item["id"] for item in result["opportunities"]}
    assert "br-fas-parentas-que-fazem" in ids
    assert "br-anmiga-mapa-articulacao-mulheres-indigenas" in ids
    assert "br-fundo-agbara-impacto-malunga" not in ids


def test_directory_can_exclude_closed_calls():
    result = WomenEconomicAutonomyDirectory().search(incluir_encerradas=False)
    assert all(
        item["status"] not in {"inscricoes_encerradas", "edicao_encerrada"}
        for item in result["opportunities"]
    )


def test_directory_rejects_invalid_filters():
    directory = WomenEconomicAutonomyDirectory()
    with pytest.raises(ValueError, match="UF"):
        directory.search(uf="São Paulo")
    with pytest.raises(ValueError, match="Público"):
        directory.search(publico="qualquer pessoa")
    with pytest.raises(ValueError, match="Tipo"):
        directory.search(tipo="emprestimo")


def test_directory_records_official_sources_and_verification_date():
    result = WomenEconomicAutonomyDirectory().search()
    assert result["count"] >= 10
    assert all(item["official_source"].startswith("https://") for item in result["opportunities"])
    assert all(item["verification_date"] == "2026-11-04" for item in result["opportunities"])
    assert "Não confunda empréstimo/crédito" in result["important_notice"]
