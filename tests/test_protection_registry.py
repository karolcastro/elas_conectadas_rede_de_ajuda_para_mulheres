import json
from datetime import date
from pathlib import Path

import pytest

from elas_conectadas_mcp.services.protection_registry import ProtectionRegistry


def test_registry_filters_by_category_and_uf(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": [
        {"id": "national", "category": "violencia_contra_mulher", "coverage": "Brasil", "verification_date": "2026-11-03"},
        {"id": "sp-local", "category": "delegacia", "coverage": "SP", "verification_date": "2026-11-03"}
    ]}), encoding="utf-8")
    registry = ProtectionRegistry(catalog, as_of=date(2026, 11, 3))
    result = registry.list_services(category="delegacia", uf="SP")
    assert [x["id"] for x in result["services"]] == ["sp-local"]


def test_registry_rejects_unknown_category(tmp_path: Path):
    registry = ProtectionRegistry(tmp_path / "empty.json")
    with pytest.raises(ValueError, match="Categoria"):
        registry.list_services(category="inventada")


def test_registry_does_not_fabricate_missing_records(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": []}), encoding="utf-8")
    result = ProtectionRegistry(catalog, as_of=date(2026, 11, 3)).list_services(uf="SP")
    assert result["count"] == 0
    assert result["services"] == []


def test_registry_filters_by_municipality_and_category():
    registry = ProtectionRegistry(as_of=date(2026, 11, 3))
    result = registry.list_services(
        uf="SP", municipality="São Paulo", category="delegacia"
    )
    assert result["count"] >= 1
    assert all(item["municipality"] == "São Paulo" for item in result["services"])
    assert all(item["official_source"].startswith("https://") for item in result["services"])
    assert all(item["catalog_status"] == "verified" for item in result["services"])
    assert all(item["review_due_date"] == "2027-02-01" for item in result["services"])


def test_registry_includes_only_publicly_listed_protection_units():
    result = ProtectionRegistry(as_of=date(2026, 11, 3)).list_services(
        uf="SP", municipality="São Paulo"
    )
    ids = {item["id"] for item in result["services"]}
    assert "sp-capital-cmb" in ids
    assert "sp-capital-ddm-1" in ids
    assert all(item.get("shelter_address_public") is False for item in result["services"])


def test_expired_records_are_hidden_by_default_and_reported(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": [
        {"id": "old", "category": "delegacia", "coverage": "SP", "verification_date": "2026-01-01"}
    ]}), encoding="utf-8")
    registry = ProtectionRegistry(catalog, as_of=date(2026, 11, 3))
    result = registry.list_services(uf="SP")
    assert result["services"] == []
    assert result["excluded_stale_count"] == 1


def test_stale_records_can_be_included_with_explicit_warning_context(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": [
        {"id": "old", "category": "delegacia", "coverage": "SP", "verification_date": "2026-01-01"}
    ]}), encoding="utf-8")
    result = ProtectionRegistry(catalog, as_of=date(2026, 11, 3)).list_services(
        uf="SP", include_stale=True
    )
    assert result["services"][0]["catalog_status"] == "expired"
    assert result["services"][0]["review_due_date"] == "2026-04-01"


def test_missing_or_invalid_verification_date_requires_review(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": [
        {"id": "unknown", "category": "delegacia", "coverage": "SP", "verification_date": "not-a-date"}
    ]}), encoding="utf-8")
    result = ProtectionRegistry(catalog, as_of=date(2026, 11, 3)).list_services(uf="SP")
    assert result["services"] == []
    assert result["excluded_stale_count"] == 1



def test_registry_returns_verified_free_services_in_rio_and_recife():
    registry = ProtectionRegistry(as_of=date(2026, 11, 4))

    rio = registry.list_services(uf="RJ", municipality="Rio de Janeiro")
    recife = registry.list_services(uf="PE", municipality="Recife")

    rio_ids = {item["id"] for item in rio["services"]}
    recife_ids = {item["id"] for item in recife["services"]}

    assert "rj-capital-ceam-chiquinha-gonzaga" in rio_ids
    assert "rj-capital-ceam-tia-gaucha" in rio_ids
    assert "pe-recife-centro-referencia-clarice-lispector" in recife_ids
    assert all(item["free"] is True for item in rio["services"])
    assert all(item["free"] is True for item in recife["services"])


def test_new_regional_records_have_sources_and_no_shelter_addresses():
    result = ProtectionRegistry(as_of=date(2026, 11, 4)).list_services(
        uf="RJ", municipality="Rio de Janeiro"
    )
    records = [
        item for item in result["services"]
        if item["id"].startswith("rj-capital-")
    ]

    assert len(records) == 2
    assert all(item["official_source"].startswith("https://") for item in records)
    assert all(item["verification_date"] == "2026-11-04" for item in records)
    assert all(item["shelter_address_public"] is False for item in records)


def test_bahia_services_without_explicit_cost_confirmation_are_not_marked_free():
    result = ProtectionRegistry(as_of=date(2026, 11, 4)).list_services(
        uf="BA", municipality="Salvador"
    )
    assert all(item.get("free") is True for item in result["services"])
    assert not any(item.get("id", "").startswith("ba-salvador-") for item in result["services"])


def test_bahia_and_pernambuco_directory_leads_do_not_claim_free_service():
    registry = ProtectionRegistry(as_of=date(2026, 11, 4))
    ba = registry.list_services(uf="BA", municipality="Lauro de Freitas")
    pe = registry.list_services(uf="PE", municipality="Olinda")

    assert ba["count"] >= 1
    assert pe["count"] >= 1
    for result in (ba, pe):
        for item in result["services"]:
            if item.get("cost_status") == "not_confirmed_by_official_source":
                assert item["free"] is None
                assert item["recommendation_status"] == "cost_confirmation_required"
        assert result["free_services_count"] >= 2
        assert result["cost_unconfirmed_count"] >= 1


def test_regional_lead_records_include_official_source_and_review_date():
    registry = ProtectionRegistry(as_of=date(2026, 11, 4))
    result = registry.list_services(uf="BA")
    leads = [x for x in result["services"] if x.get("cost_status") == "not_confirmed_by_official_source"]
    assert len(leads) >= 25
    assert all(x["official_source"].startswith("https://") for x in leads)
    assert all(x["free"] is None for x in leads)
    assert all(x["shelter_address_public"] is False for x in leads)
