import json
from pathlib import Path

import pytest

from elas_conectadas_mcp.services.protection_registry import ProtectionRegistry


def test_registry_filters_by_category_and_uf(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": [
        {"id": "national", "category": "violencia_contra_mulher", "coverage": "Brasil"},
        {"id": "sp-local", "category": "delegacia", "coverage": "SP"}
    ]}), encoding="utf-8")
    registry = ProtectionRegistry(catalog)
    result = registry.list_services(category="delegacia", uf="SP")
    assert [x["id"] for x in result["services"]] == ["sp-local"]

def test_registry_rejects_unknown_category(tmp_path: Path):
    registry = ProtectionRegistry(tmp_path / "empty.json")
    with pytest.raises(ValueError, match="Categoria"):
        registry.list_services(category="inventada")

def test_registry_does_not_fabricate_missing_records(tmp_path: Path):
    catalog = tmp_path / "services.json"
    catalog.write_text(json.dumps({"records": []}), encoding="utf-8")
    result = ProtectionRegistry(catalog).list_services(uf="SP")
    assert result["count"] == 0
    assert result["services"] == []


def test_registry_filters_by_municipality_and_category():
    registry = ProtectionRegistry()
    result = registry.list_services(
        uf="SP", municipality="São Paulo", category="delegacia"
    )
    assert result["count"] >= 1
    assert all(item["municipality"] == "São Paulo" for item in result["services"])
    assert all(item["official_source"].startswith("https://") for item in result["services"])
    assert all(item["verification_date"] == "2026-11-03" for item in result["services"])


def test_registry_includes_only_publicly_listed_protection_units():
    result = ProtectionRegistry().list_services(uf="SP", municipality="São Paulo")
    ids = {item["id"] for item in result["services"]}
    assert "sp-capital-cmb" in ids
    assert "sp-capital-ddm-1" in ids
    assert all(item.get("shelter_address_public") is False for item in result["services"])
