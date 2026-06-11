from __future__ import annotations

import csv
import io
import logging
from typing import Any
from uuid import UUID

try:
    from arq.connections import RedisSettings
except ImportError:

    class RedisSettings:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass


from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.db.session import get_sessionmaker
from app.models import ExportJob, ImportJob, User, UserStatus
from app.services.file_admin import FileAdminService
from app.services.user_admin import RoleNotFoundError, UserAdminService
from app.storage.minio import build_minio_client

logger = logging.getLogger("arq.worker")


async def startup(ctx: dict[str, Any]) -> None:
    settings = get_settings()
    ctx["session_factory"] = get_sessionmaker()
    ctx["minio_client"] = build_minio_client(settings)
    logger.info("Arq background worker started up successfully.")


async def shutdown(ctx: dict[str, Any]) -> None:
    logger.info("Arq background worker shutting down.")


async def import_users_task(ctx: dict[str, Any], job_id: UUID) -> None:
    session_factory = ctx["session_factory"]
    minio_client = ctx["minio_client"]

    async with session_factory() as session:
        # 1. Fetch import job
        stmt = select(ImportJob).where(ImportJob.id == job_id).options(selectinload(ImportJob.file))
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()

        if not job:
            logger.error(f"Import job {job_id} not found.")
            return

        if job.status != "pending":
            logger.warning(f"Import job {job_id} is already in state {job.status}.")
            return

        job.status = "processing"
        await session.commit()

        # 2. Get file stream from MinIO
        try:
            minio_response = minio_client.get_object(
                bucket_name=job.file.bucket,
                object_name=job.file.storage_path,
            )
            try:
                content = minio_response.read()
            finally:
                minio_response.close()
                minio_response.release_conn()

            csv_text = content.decode("utf-8-sig")
            csv_file = io.StringIO(csv_text)
            reader = csv.DictReader(csv_file)
            rows = list(reader)
        except Exception as e:
            logger.exception(f"Failed to read/parse CSV file for import job {job_id}")
            job.status = "failed"
            job.error_summary = f"Failed to read/parse CSV: {e}"
            await session.commit()
            return

        job.total_rows = len(rows)
        await session.commit()

        user_service = UserAdminService(session)
        processed_rows = 0
        failed_rows = 0
        errors_list = []

        # 3. Process each row
        for idx, row in enumerate(rows, start=1):
            email = (row.get("email") or "").strip()
            password = row.get("password") or ""
            status_str = (row.get("status") or "").strip().lower()
            roles_str = row.get("roles") or ""
            full_name = (row.get("full_name") or row.get("fullName") or "").strip()

            # Standard defaults
            status = UserStatus.ACTIVE
            if status_str:
                try:
                    status = UserStatus(status_str)
                except ValueError:
                    errors_list.append(
                        {
                            "row": idx,
                            "email": email,
                            "errors": [f"Invalid status '{status_str}'."],
                        }
                    )
                    failed_rows += 1
                    continue

            # Default roles list
            role_names = [r.strip() for r in roles_str.split(",") if r.strip()]
            if not role_names:
                role_names = ["user"]

            # Validation checks before database call
            row_errors = []
            if not email:
                row_errors.append("Email is required.")
            if not password or len(password) < 8:
                row_errors.append("Password must be at least 8 characters long.")
            if not full_name:
                row_errors.append("Full name is required.")

            if row_errors:
                errors_list.append({"row": idx, "email": email, "errors": row_errors})
                failed_rows += 1
                continue

            # Database creation inside nested sub-transaction
            try:
                async with session.begin_nested():
                    await user_service.create_user(
                        email=email,
                        password=password,
                        status=status,
                        role_names=role_names,
                        full_name=full_name,
                    )
                processed_rows += 1
            except RoleNotFoundError as e:
                errors_list.append({"row": idx, "email": email, "errors": [str(e)]})
                failed_rows += 1
            except Exception as e:
                # Catch duplicates or other database constraints
                # If email already exists or similar database constraint raised
                # Check for standard unique email constraint error message
                msg = str(e)
                if "already exists" in msg or "unique constraint" in msg.lower():
                    msg = f"User with email {email} already exists."
                errors_list.append({"row": idx, "email": email, "errors": [msg]})
                failed_rows += 1

            # Update job progress periodically
            if idx % 10 == 0 or idx == len(rows):
                job.processed_rows = processed_rows
                job.failed_rows = failed_rows
                job.errors_json = errors_list
                await session.commit()

        # 4. Finish import job
        job.status = "completed" if failed_rows < len(rows) else "failed"
        if failed_rows == len(rows):
            job.error_summary = "All rows failed to import."
        job.processed_rows = processed_rows
        job.failed_rows = failed_rows
        job.errors_json = errors_list
        await session.commit()


async def export_users_task(ctx: dict[str, Any], job_id: UUID) -> None:
    session_factory = ctx["session_factory"]
    minio_client = ctx["minio_client"]

    async with session_factory() as session:
        # 1. Fetch export job
        stmt = select(ExportJob).where(ExportJob.id == job_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()

        if not job:
            logger.error(f"Export job {job_id} not found.")
            return

        job.status = "processing"
        await session.commit()

        try:
            filters = job.filters or {}

            # 2. Query matching users
            query = select(User).options(selectinload(User.roles))
            if search := filters.get("search"):
                query = query.where(User.email.ilike(f"%{search}%"))
            if status_str := filters.get("status"):
                query = query.where(User.status == UserStatus(status_str))

            query = query.order_by(User.created_at.desc())
            users_result = await session.execute(query)
            users = users_result.scalars().all()

            # 3. Generate CSV in-memory
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["email", "status", "roles", "created_at"])

            for user in users:
                roles_str = ",".join([r.name for r in user.roles])
                writer.writerow(
                    [user.email, user.status.value, roles_str, user.created_at.isoformat()]
                )

            csv_bytes = csv_buffer.getvalue().encode("utf-8")
            csv_stream = io.BytesIO(csv_bytes)

            # 4. Upload file to MinIO (marked as private)
            file_admin = FileAdminService(session, minio_client)
            db_file = await file_admin.upload_file(
                filename=f"users_export_{job_id}.csv",
                content_type="text/csv",
                size_bytes=len(csv_bytes),
                data_stream=csv_stream,
                is_public=False,
                uploaded_by_id=job.created_by_id,
            )

            # 5. Link file to export job
            job.file_id = db_file.id
            job.status = "completed"
            await session.commit()
        except Exception as e:
            logger.exception(f"Failed to export users for job {job_id}")
            job.status = "failed"
            job.error_summary = str(e)
            await session.commit()


settings = get_settings()


class WorkerSettings:
    redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
    functions = [import_users_task, export_users_task]
    on_startup = startup
    on_shutdown = shutdown
