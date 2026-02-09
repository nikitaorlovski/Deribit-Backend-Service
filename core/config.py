from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    db_name: str
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"), env_file_encoding="utf-8"
    )

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def sqlalchemy_url(self):
        return f"postgresql+psycopg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
