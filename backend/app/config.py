from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_url: str = "postgresql://DeepTrace AI:DeepTrace AI_secret@localhost:5432/DeepTrace AI"
    redis_url: str = "redis://localhost:6379"
    kafka_bootstrap_servers: str = "localhost:9092"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    openai_api_key: str = ""


settings = Settings()
