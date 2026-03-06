"""
SK Framework — Configuration
Loads and validates all settings from environment / .env file.
"""

import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Auto-load .env from project root
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
if ENV_PATH.exists():
    from dotenv import load_dotenv
    load_dotenv(ENV_PATH)


class LLMProviderConfig(BaseSettings):
    """Keys and defaults for each supported LLM provider."""
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class APIConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="SK_API_"
    )


class DatabaseConfig(BaseSettings):
    db_path: str = "./data/sk_sessions.db"

    model_config = SettingsConfigDict(
        env_prefix="SK_"
    )


class LogConfig(BaseSettings):
    log_level: str = "INFO"
    log_format: str = "json"  # json | text

    model_config = SettingsConfigDict(
        env_prefix="SK_"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()


class LabConfig(BaseSettings):
    lab_timeout_seconds: int = 300
    lab_max_attempts: int = 10

    model_config = SettingsConfigDict(
        env_prefix="SK_"
    )


class SKConfig(BaseSettings):
    """Root configuration object. Import this everywhere."""

    # Core
    default_provider: str = "openai"
    default_model: str = "gpt-4o"
    dry_run: bool = False

    # Sub-configs
    llm: LLMProviderConfig = LLMProviderConfig()
    api: APIConfig = APIConfig()
    db: DatabaseConfig = DatabaseConfig()
    log: LogConfig = LogConfig()
    lab: LabConfig = LabConfig()

    model_config = SettingsConfigDict(
        env_prefix="SK_"
    )

    @field_validator("default_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        allowed = {"openai", "anthropic", "google"}
        if v.lower() not in allowed:
            raise ValueError(f"default_provider must be one of {allowed}")
        return v.lower()

    def get_api_key(self, provider: str) -> str | None:
        """Get the API key for a given provider."""
        mapping = {
            "openai": self.llm.openai_api_key,
            "anthropic": self.llm.anthropic_api_key,
            "google": self.llm.google_api_key,
        }
        return mapping.get(provider.lower())

    def has_provider(self, provider: str) -> bool:
        """Check if a provider is configured (has an API key)."""
        return self.get_api_key(provider) is not None

    def available_providers(self) -> list[str]:
        """Return list of providers that have API keys configured."""
        return [p for p in ["openai", "anthropic", "google"] if self.has_provider(p)]


# Singleton — import this anywhere in the app
config = SKConfig()
