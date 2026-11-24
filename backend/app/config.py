from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_url: str = "postgresql://DeepTrace AI:DeepTrace AI_secret@localhost:5432/DeepTrace AI"
    redis_url: str = "redis://localhost:6379"
    kafka_bootstrap_servers: str = "localhost:9092"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"


settings = Settings()
