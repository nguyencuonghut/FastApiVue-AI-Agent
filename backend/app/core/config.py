from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_name: str = Field(default="FastApiVueBoilerplate", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    app_version: str = "0.1.0"
    app_timezone: str = Field(default="Asia/Ho_Chi_Minh", alias="APP_TIMEZONE")

    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")  # nosec B104
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    jwt_secret_key: str = Field(default="change-me", alias="JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = Field(
        default="change-me-too",
        alias="JWT_REFRESH_SECRET_KEY",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )
    auth_token_transport: str = Field(default="hybrid", alias="AUTH_TOKEN_TRANSPORT")
    auth_refresh_cookie_name: str = Field(
        default="fastapivue_refresh_token",
        alias="AUTH_REFRESH_COOKIE_NAME",
    )
    auth_logged_in_cookie_name: str = Field(
        default="fastapivue_logged_in",
        alias="VITE_AUTH_LOGGED_IN_COOKIE_NAME",
    )
    auth_refresh_cookie_secure: bool = Field(
        default=False,
        alias="AUTH_REFRESH_COOKIE_SECURE",
    )
    auth_refresh_cookie_samesite: Literal["lax", "strict", "none"] = Field(
        default="lax",
        alias="AUTH_REFRESH_COOKIE_SAMESITE",
    )
    auth_refresh_cookie_path: str = Field(
        default="/api/v1/auth",
        alias="AUTH_REFRESH_COOKIE_PATH",
    )
    auth_seed_admin_email: str = Field(
        default="admin@fastapivue.local",
        alias="AUTH_SEED_ADMIN_EMAIL",
    )
    auth_seed_admin_password: str = Field(
        default="change-me-admin-password",
        alias="AUTH_SEED_ADMIN_PASSWORD",
    )
    auth_seed_update_admin_password: bool = Field(
        default=False,
        alias="AUTH_SEED_UPDATE_ADMIN_PASSWORD",
    )

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@postgres:5432/app",
        alias="DATABASE_URL",
    )

    minio_endpoint: str = Field(default="minio:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", alias="MINIO_SECRET_KEY")
    minio_bucket: str = Field(default="app-local", alias="MINIO_BUCKET")
    minio_secure: bool = Field(default=False, alias="MINIO_SECURE")

    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    cors_origins: str = Field(
        default="http://127.0.0.1:5173,http://localhost:5173",
        alias="CORS_ORIGINS",
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
