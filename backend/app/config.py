from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./jee_mentor.db"
    frontend_origin: str = "http://localhost:5173"

    foundry_project_endpoint: str | None = None
    foundry_agent_id: str | None = None
    foundry_iq_endpoint: str | None = None
    foundry_iq_api_key: str | None = None
    foundry_iq_knowledge_base_id: str | None = None
    tesseract_cmd: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def foundry_enabled(self) -> bool:
        return bool(self.foundry_project_endpoint and self.foundry_agent_id)

    @property
    def foundry_iq_enabled(self) -> bool:
        return bool(
            self.foundry_iq_endpoint
            and self.foundry_iq_api_key
            and self.foundry_iq_knowledge_base_id
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
