from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Application
    app_name: str = "AI Research Copilot"
    app_env: Literal["development", "testing", "production"] = "development"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    # LLM Configuration
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    default_llm_provider: Literal["anthropic", "openai"] = "anthropic"
    default_model_name: str = "claude-3-5-sonnet-20241022"

    # Web Search
    tavily_api_key: str | None = None

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/research_copilot"
    )
    checkpoint_db_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/research_copilot"
    )

    # Observability
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_host: str = "https://cloud.langfuse.com"

    # Guardrails
    max_research_loops: int = 3
    max_token_budget: int = 100_000


@lru_cache
def get_settings() -> Settings:
    """Singleton getter for cached configuration settings."""
    return Settings()
