from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.models import ExportJob, File, ImportJob, Role, User, UserStatus
from app.worker import export_users_task, import_users_task


class FakeMinioResponse:
    def __init__(self, data: bytes) -> None:
        self.data = data

    def read(self) -> bytes:
        return self.data

    def close(self) -> None:
        pass

    def release_conn(self) -> None:
        pass


class FakeNestedTransaction:
    async def __aenter__(self) -> FakeNestedTransaction:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is not None:
            raise exc_val


class FakeAsyncSession:
    def __init__(
        self,
        *,
        import_job: ImportJob | None = None,
        export_job: ExportJob | None = None,
        roles: list[Any] | None = None,
        users: list[User] | None = None,
    ) -> None:
        self.import_job = import_job
        self.export_job = export_job
        self.roles = roles or []
        self.users = users or []
        self.added: list[object] = []
        self.committed = False

    async def execute(self, statement: object) -> MagicMock:
        compiled = str(statement)
        result = MagicMock()

        if "FROM import_jobs" in compiled:
            result.scalar_one_or_none.return_value = self.import_job
        elif "FROM export_jobs" in compiled:
            result.scalar_one_or_none.return_value = self.export_job
        elif "FROM roles" in compiled:
            result.scalars.return_value.all.return_value = self.roles
        elif "FROM users" in compiled:
            # Simple mock for get_user_by_email
            params = statement.compile().params  # type: ignore[attr-defined]
            email = params.get("email_1")
            existing = None
            if email:
                for u in self.users:
                    if u.email == email:
                        existing = u
            result.scalar_one_or_none.return_value = existing
            result.scalars.return_value.all.return_value = self.users

        return result

    def add(self, instance: object) -> None:
        self.added.append(instance)

    async def commit(self) -> None:
        self.committed = True

    async def flush(self) -> None:
        pass

    def begin_nested(self) -> FakeNestedTransaction:
        return FakeNestedTransaction()

    async def __aenter__(self) -> FakeAsyncSession:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


@pytest.mark.asyncio
async def test_import_users_task_success() -> None:
    job_id = uuid4()
    db_file = File(
        id=uuid4(),
        filename="import.csv",
        bucket="bucket",
        storage_path="x/import.csv",
        content_type="text/csv",
        size_bytes=100,
    )
    job = ImportJob(id=job_id, file_id=db_file.id, status="pending")
    job.file = db_file

    session = FakeAsyncSession(import_job=job, roles=[Role(id=uuid4(), name="user")])
    session_factory = MagicMock()
    session_factory.return_value = session

    minio_client = MagicMock()
    # CSV with 1 header, 2 rows (1 success, 1 failure due to short password)
    csv_data = (
        b"email,password,status,roles\n"
        b"success@example.com,pass12345,active,user\n"
        b"fail@example.com,short,active,user"
    )
    minio_client.get_object.return_value = FakeMinioResponse(csv_data)

    ctx = {
        "session_factory": session_factory,
        "minio_client": minio_client,
    }

    await import_users_task(ctx, job_id)

    assert job.status == "completed"
    assert job.total_rows == 2
    assert job.processed_rows == 1
    assert job.failed_rows == 1
    assert job.errors_json is not None
    assert len(job.errors_json) == 1
    assert job.errors_json[0]["email"] == "fail@example.com"
    assert "Password must be at least 8 characters" in job.errors_json[0]["errors"][0]


@pytest.mark.asyncio
async def test_export_users_task_success() -> None:
    job_id = uuid4()
    job = ExportJob(
        id=job_id,
        status="pending",
        created_by_id=uuid4(),
        filters={"status": "active"},
    )

    u1 = User(id=uuid4(), email="u1@example.com", status=UserStatus.ACTIVE, created_at=MagicMock())
    u1.roles = []
    session = FakeAsyncSession(export_job=job, users=[u1])
    session_factory = MagicMock()
    session_factory.return_value = session

    minio_client = MagicMock()
    ctx = {
        "session_factory": session_factory,
        "minio_client": minio_client,
    }

    await export_users_task(ctx, job_id)

    assert job.status == "completed"
    assert job.file_id is not None
    # Verify minio upload was called
    assert minio_client.put_object.call_count == 1
