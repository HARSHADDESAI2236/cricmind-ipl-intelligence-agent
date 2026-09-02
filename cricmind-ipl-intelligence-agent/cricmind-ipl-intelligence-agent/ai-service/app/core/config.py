"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-4-5"
    database_url: str = "postgresql://cricmind:cricmind@localhost:5432/cricmind"
    embedding_dim: int = 1536
    app_name: str = "CricMind AI Service"
    cors_origins: list[str] = ["*"]


settings = Settings()
