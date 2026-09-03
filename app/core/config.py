from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    APP_NAME        : str = "ExperimentOS"
    APP_VERSION     : str = "1.0.9"

    USER_NAME       : str = ""

    POSTGRES_URL    : str = ""
    REDIS_URL       : str = ""
    RABBITMQ_URL    : str = ""

    SMTP_HOST       : str = ""
    SMTP_PORT       : int = 0
    SMTP_USERNAME   : str = ""
    SMTP_PASSWORD   : str = ""
    SMTP_FROM_EMAIL : str = ""
    SMTP_FROM_NAME  : str = "ExperimentOS"

    JWT_SECRET_KEY  : str = ""
    JWT_ALGORITHM   : str = "HS256"
    JWT_ISSUER      : str = "ExperimentOS"
    JWT_AUDIENCE    : str = "ExperimentOS-API"

    ACCESS_TOKEN_EXPIRE_SECONDS     : int = 900
    REFRESH_TOKEN_EXPIRE_SECONDS    : int = 7*24*3600


    model_config = SettingsConfigDict(
        env_file = ".env",
        extra    = "ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() 