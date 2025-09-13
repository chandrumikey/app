from pydantic_settings import BaseSettings,      SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    # Database
    DB_DRIVER: str = "postgresql+psycopg2"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "prototype_tm"

settings = Settings()