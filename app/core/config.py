"""Central settings. Values come from environment / .env — never hardcode secrets."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Runtime
    ENV: str = "local"                      # local | dev | qa | uat | prod
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = "http://localhost:5173"

    # Database / cache
    DATABASE_URL: str = "postgresql+psycopg://healthekit:healthekit@localhost:5432/healthekit"
    REDIS_URL: str = "redis://localhost:6379/0"

    # ABDM Sandbox / Production gateway
    ABDM_CLIENT_ID: str = "SBXID_043801"
    ABDM_CLIENT_SECRET: str = "CHANGE_ME"   # Jenkins credential / AWS SSM in real envs
    ABDM_GATEWAY_BASE: str = "https://dev.abdm.gov.in/api/hiecm"
    ABHA_BASE: str = "https://abhasbx.abdm.gov.in/abha/api"
    ABDM_X_CM_ID: str = "sbx"
    ABDM_HIP_ID: str = "CHANGE_ME"          # your registered HIP service id
    ABDM_HIU_ID: str = "CHANGE_ME"

    # App security
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
