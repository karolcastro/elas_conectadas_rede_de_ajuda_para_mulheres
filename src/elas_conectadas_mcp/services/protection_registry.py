"""Consulta catálogo curado de serviços com validação de fonte e cobertura."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).resolve().parents[3] / "data" / "servicos_protecao.json"
ALLOWED_CATEGORIES = {
    "emergencia", "violencia_contra_mulher", "delegacia",
    "assistencia_juridica", "acolhimento", "ong", "apoio_psicossocial",
}


class ProtectionRegistry:
    """Lê registros verificados; não inventa nem completa dados ausentes."""

    def __init__(self, catalog_path: Path | None = None) -> None:
        self.catalog_path = catalog_path or CATALOG_PATH

    def list_services(
        self, *, category: str | None = None, uf: str | None = None,
        municipality: str | None = None,
    ) -> dict[str, Any]:
        if category and category not in ALLOWED_CATEGORIES:
            raise ValueError("Categoria de serviço inválida.")
        if uf and (len(uf.strip()) != 2 or not uf.strip().isalpha()):
            raise ValueError("Informe uma sigla de UF válida com duas letras.")
        if municipality and len(municipality.strip()) < 2:
            raise ValueError("Informe um município válido.")
        try:
            payload = json.loads(self.catalog_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError("Catálogo de serviços indisponível ou inválido.") from exc
        selected = []
        normalized_uf = uf.strip().upper() if uf else None
        normalized_municipality = municipality.strip().casefold() if municipality else None
        for item in payload.get("records", []):
            if category and item.get("category") != category:
                continue
            coverage = str(item.get("coverage", ""))
            if uf and coverage not in {"Brasil", normalized_uf} and normalized_uf not in item.get("ufs", []):
                continue
            if municipality and str(item.get("municipality", "")).casefold() != normalized_municipality:
                continue
            selected.append(item)
        return {
            "services": selected,
            "count": len(selected),
            "filters": {"category": category, "uf": normalized_uf, "municipality": municipality.strip() if municipality else None},
            "catalog_source": "Catálogo curado do projeto; cada registro contém sua fonte oficial e data de verificação.",
            "important_notice": (
                "A lista contém apenas registros cadastrados e validados. Ausência de resultado não significa "
                "inexistência de serviço na região. Confirme funcionamento, critérios e disponibilidade "
                "diretamente com o órgão responsável. A proximidade não é calculada."
            ),
        }

    def national_emergency_channels(self) -> dict[str, Any]:
        result = self.list_services()
        return {
            "services": [
                item for item in result["services"]
                if item.get("category") in {"emergencia", "violencia_contra_mulher"}
            ],
            "important_notice": result["important_notice"],
        }
