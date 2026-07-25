"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Central application settings."""

    model_config = SettingsConfigDict(env_prefix="BLUESHIELD_", env_file=".env", extra="ignore")

    app_name: str = "BlueShield Auditor API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    database_url: str = f"sqlite:///{BACKEND_DIR / 'blueshield.db'}"

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    # Vite falls back to another port (or IPv6 ::1) if 5173 is taken, so dev CORS
    # matches any localhost/127.0.0.1/[::1] origin regardless of port.
    cors_origin_regex: str = r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$"

    log_level: str = "INFO"

    reports_dir: Path = BACKEND_DIR / "generated_reports"

    # Default audit mode when the client doesn't specify one. "real" runs actual
    # Windows commands; individual checks still fall back to simulated data if
    # the real check fails (no admin rights, non-Windows host, command missing).
    default_audit_mode: str = "real"

    command_timeout_seconds: int = 15


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
