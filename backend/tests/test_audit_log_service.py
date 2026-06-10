from __future__ import annotations

from uuid import uuid4

import pytest

from app.services.audit_log import AuditLogContext, AuditLogService


class FakeAsyncSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.flush_count = 0

    def add(self, instance: object) -> None:
        self.added.append(instance)

    async def flush(self) -> None:
        self.flush_count += 1


@pytest.mark.asyncio
async def test_log_event_persists_audit_record() -> None:
    session = FakeAsyncSession()
    service = AuditLogService(session)  # type: ignore[arg-type]
    actor_user_id = uuid4()

    audit_log = await service.log_event(
        action="auth.login_succeeded",
        entity_type="user",
        context=AuditLogContext(
            actor_user_id=actor_user_id,
            entity_id=str(actor_user_id),
            ip_address="127.0.0.1",
            metadata_json={"email": "admin@example.com"},
            request_id="req-123",
        ),
    )

    assert audit_log.actor_user_id == actor_user_id
    assert audit_log.action == "auth.login_succeeded"
    assert audit_log.entity_type == "user"
    assert audit_log.request_id == "req-123"
    assert len(session.added) == 1
    assert session.flush_count == 1
