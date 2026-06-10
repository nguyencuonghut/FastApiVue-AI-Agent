from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.request_id import request_id_context
from app.models import AuditLog


@dataclass(slots=True, frozen=True)
class AuditLogContext:
    actor_user_id: UUID | None = None
    entity_id: str | None = None
    ip_address: str | None = None
    metadata_json: dict[str, object] | None = None
    request_id: str | None = None


class AuditLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def log_event(
        self,
        *,
        action: str,
        entity_type: str,
        context: AuditLogContext | None = None,
    ) -> AuditLog:
        resolved_context = context or AuditLogContext()
        audit_log = AuditLog(
            actor_user_id=resolved_context.actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=resolved_context.entity_id,
            request_id=resolved_context.request_id or request_id_context.get() or None,
            ip_address=resolved_context.ip_address,
            metadata_json=resolved_context.metadata_json,
        )
        self.session.add(audit_log)
        await self.session.flush()
        return audit_log
