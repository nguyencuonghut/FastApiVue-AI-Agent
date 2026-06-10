from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging
from app.core.request_id import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    app.state.settings = settings

    try:
        from app.storage.minio import build_minio_client

        minio_client = build_minio_client(settings)
        bucket = settings.minio_bucket
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)
    except Exception as e:
        import logging

        logging.getLogger("app").warning(
            f"Could not connect or initialize MinIO bucket '{settings.minio_bucket}': {e}"
        )

    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    app = FastAPI(
        title=app_settings.app_name,
        debug=app_settings.app_debug,
        version=app_settings.app_version,
        lifespan=lifespan,
    )
    app.add_middleware(RequestIDMiddleware)
    app.include_router(api_router, prefix=app_settings.api_v1_prefix)

    @app.get("/health", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {
            "status": "ok",
            "service": app_settings.app_name,
            "environment": app_settings.app_env,
        }

    return app
