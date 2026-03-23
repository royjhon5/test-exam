from __future__ import annotations

from typing import Any

TENANT_ALERTS: dict[str, list[dict[str, Any]]] = {
    "tenant-acme": [
        {
            "id": "acme-1001",
            "tenant_id": "tenant-acme",
            "severity": "high",
            "status": "open",
            "source": "identity",
            "title": "Impossible travel login detected",
            "description": "A privileged user logged in from two distant geographies within 12 minutes.",
            "created_at": "2026-03-20T10:15:00Z",
        },
        {
            "id": "acme-1002",
            "tenant_id": "tenant-acme",
            "severity": "medium",
            "status": "investigating",
            "source": "endpoint",
            "title": "Unsigned binary launched on finance workstation",
            "description": "A newly seen executable spawned PowerShell with encoded arguments.",
            "created_at": "2026-03-21T07:42:00Z",
        },
    ],
    "tenant-globex": [
        {
            "id": "globex-2001",
            "tenant_id": "tenant-globex",
            "severity": "critical",
            "status": "open",
            "source": "cloud",
            "title": "Public storage bucket with customer exports",
            "description": "A cloud storage bucket was modified to allow anonymous reads.",
            "created_at": "2026-03-19T16:03:00Z",
        },
        {
            "id": "globex-2002",
            "tenant_id": "tenant-globex",
            "severity": "low",
            "status": "resolved",
            "source": "email",
            "title": "Phishing simulation click",
            "description": "An employee clicked a simulated phishing email during awareness training.",
            "created_at": "2026-03-22T13:27:00Z",
        },
    ],
}
