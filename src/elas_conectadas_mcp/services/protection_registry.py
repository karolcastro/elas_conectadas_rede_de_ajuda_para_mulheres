"""Consulta catálogo curado com controle de validade da verificação."""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).resolve().parents[3] / "data" / "servicos_protecao.json"
ALLOWED_CATEGORIES = {
    "emergencia", "violencia_contra_mulher", "delegacia",
    "assistencia_juridica", "acolhimento", "ong", "apoio_psicossocial",
}
REVIEW_INTERVAL_DAYS = 90


class ProtectionRegistry:
    """Lê registros com fonte oficial e sinaliza verificações vencidas."""

    def __init__(
        self, catalog_path: Path | None = None, *, as_of: date | None = None
    ) -> None:
        self.catalog_path = catalog_path or CATALOG_PATH
        self.as_of = as_of or date.today()

    def _verification_metadata(self, item: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(item)
        raw_date = item.get("verification_date")
        try:
            verified_on = date.fromisoformat(raw_date) if raw_date else None
        except (TypeError, ValueError):
            verified_on = None
        if verified_on is None:
            due_date = None
            status = "needs_review"
        else:
            due_date = verified_on + timedelta(days=REVIEW_INTERVAL_DAYS)
            status = "verified" if self.as_of <= due_date else "expired"
        enriched["review_due_date"] = due_date.isoformat() if due_date else None
        enriched["catalog_status"] = status
        return enriched

    def list_services(
        self, *, category: str | None = None, uf: str | None = None,
        municipality: str | None = None, include_stale: bool = False,
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
        excluded_stale = 0
        normalized_uf = uf.strip().upper() if uf else None
        normalized_municipality = municipality.strip().casefold() if municipality else None
        for raw_item in payload.get("records", []):
            item = self._verification_metadata(raw_item)
            if category and item.get("category") != category:
                continue
            coverage = str(item.get("coverage", ""))
            if uf and coverage not in {"Brasil", normalized_uf} and normalized_uf not in item.get("ufs", []):
                continue
            if municipality and str(item.get("municipality", "")).casefold() != normalized_municipality:
                continue
            if item["catalog_status"] != "verified" and not include_stale:
                excluded_stale += 1
                continue
            selected.append(item)
        return {
            "services": selected,
            "count": len(selected),
            "excluded_stale_count": excluded_stale,
            "as_of": self.as_of.isoformat(),
            "filters": {
                "category": category, "uf": normalized_uf,
                "municipality": municipality.strip() if municipality else None,
                "include_stale": include_stale,
            },
            "catalog_source": "Catálogo curado; cada registro informa fonte oficial, data de verificação e prazo de revisão.",
            "important_notice": (
                "Por padrão, registros sem data válida ou com revisão vencida são omitidos. "
                "A data de revisão é um controle editorial, não uma confirmação automática de funcionamento. "
                "Confirme funcionamento, critérios e disponibilidade diretamente com o órgão responsável. "
                "Ausência de resultado não significa inexistência de serviço; a proximidade não é calculada."
            ),
        }

    def national_emergency_channels(self) -> dict[str, Any]:
        result = self.list_services()
        return {
            "services": [
                item for item in result["services"]
                if item.get("category") in {"emergencia", "violencia_contra_mulher"}
            ],
            "excluded_stale_count": result["excluded_stale_count"],
            "as_of": result["as_of"],
            "important_notice": result["important_notice"],
        }
