"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_PUBLISHABLE_KEY: str
    SUPABASE_SECRET_KEY: str

    # API Keys
    GEMINI_API_KEY: str = ""

    # Application
    PROJECT_NAME: str = "EPL Fantasy Forward API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # FPL API
    FPL_API_ENDPOINT: str = "https://fantasy.premierleague.com/api/bootstrap-static/"
    CACHE_TTL_SECONDS: int = 600
    
    # Rate Limiting
    AI_REQUESTS_PER_HOUR: int = 20
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()
