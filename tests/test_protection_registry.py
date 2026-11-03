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
