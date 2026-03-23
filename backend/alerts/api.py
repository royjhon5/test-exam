from __future__ import annotations

from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel

from .services import TenantAccessError, get_tenant_alerts

router = Router(tags=["alerts"])


class EnrichmentSchema(BaseModel):
    summary: str
    risk_score: int
    recommended_action: str
    model: str


class AlertSchema(BaseModel):
    id: str
    tenant_id: str
    severity: str
    status: str
    source: str
    title: str
    description: str
    created_at: str
    enrichment: EnrichmentSchema


class AlertListSchema(BaseModel):
    items: list[AlertSchema]
    page: int
    page_size: int
    total: int
    total_pages: int
    tenant_id: str
    role: str


@router.get("alerts", response=AlertListSchema)
def list_alerts(request, page: int = 1, page_size: int = 25):
    tenant_id = request.headers.get("x-tenant-id")
    role = request.headers.get("x-user-role", "analyst")

    if not tenant_id:
        raise HttpError(401, "Missing X-Tenant-Id header")

    try:
        return get_tenant_alerts(tenant_id=tenant_id, role=role, page=page, page_size=page_size)
    except TenantAccessError as exc:
        raise HttpError(403, str(exc)) from exc
