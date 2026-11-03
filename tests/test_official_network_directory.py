from __future__ import annotations

import pytest

from elas_conectadas_mcp.services.official_network_directory import (
    PANEL_SERVICE_TYPES,
    OfficialNetworkDirectory,
)

def test_guide_returns_official_panel_and_does_not_claim_automated_results():
    result = OfficialNetworkDirectory().guide(uf="SP", municipality="São Paulo")
    assert result["official_panel_url"].startswith("https://www.gov.br/")
    assert result["search_filters_requested"]["uf"] == "SP"
    assert result["automated_records_available"] is False
    assert result["integration_status"] == "official_link_and_guidance_only"

def test_guide_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        OfficialNetworkDirectory().guide(uf="São Paulo")

def test_guide_rejects_unknown_service_type():
    with pytest.raises(ValueError, match="Tipo de serviço"):
        OfficialNetworkDirectory().guide(category="serviço inventado")

def test_panel_service_categories_are_present():
    result = OfficialNetworkDirectory().guide()
    assert result["known_service_types"] == PANEL_SERVICE_TYPES
