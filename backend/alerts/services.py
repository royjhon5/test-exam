from __future__ import annotations

from math import ceil
from typing import Any

from .data import TENANT_ALERTS


class TenantAccessError(PermissionError):
    """Raised when tenant headers are missing or invalid."""


VALID_ROLES = {"admin", "analyst"}


def mock_llm_enrichment(alert: dict[str, Any]) -> dict[str, Any]:
    severity_score = {"low": 25, "medium": 55, "high": 80, "critical": 95}[alert["severity"]]
    summary = (
        f"{alert['title']}: prioritize {alert['source']} triage for tenant {alert['tenant_id']} "
        f"with a risk score of {severity_score}."
    )
    return {
        **alert,
        "enrichment": {
            "summary": summary,
            "risk_score": severity_score,
            "recommended_action": "Escalate to admin for containment" if severity_score >= 80 else "Review evidence and close or escalate",
            "model": "mock-llm-v1",
        },
    }


def get_tenant_alerts(tenant_id: str, role: str, page: int = 1, page_size: int = 25) -> dict[str, Any]:
    if tenant_id not in TENANT_ALERTS:
        raise TenantAccessError("Unknown tenant")
    if role not in VALID_ROLES:
        raise TenantAccessError("Invalid role")

    alerts = [mock_llm_enrichment(alert) for alert in TENANT_ALERTS[tenant_id]]
    total = len(alerts)
    total_pages = max(1, ceil(total / page_size))
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": alerts[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "tenant_id": tenant_id,
        "role": role,
    }
