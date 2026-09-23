from functools import lru_cache

from pydantic import SecretStr

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    APP_NAME         : str = "QueryLens.AI"
    APP_VERSION      : str = "2.0.0"

    USER_NAME        : str = ""

    POSTGRES_URL     : str = ""
    REDIS_URL        : str = ""
    RABBITMQ_URL     : str = ""

    SMTP_HOST        : str = ""
    SMTP_PORT        : int = 0
    SMTP_USERNAME    : str = ""
    SMTP_PASSWORD    : str = ""
    SMTP_FROM_EMAIL  : str = ""
    SMTP_FROM_NAME   : str = ""

    JWT_SECRET_KEY   : str = ""
    JWT_ALGORITHM    : str = ""
    JWT_ISSUER       : str = ""
    JWT_AUDIENCE     : str = ""

    SELECTED_MODEL   : str = ""
    RETRY_COUNT      : int = 3

    EXPERIMENT_QUEUE : str = ""

    OPENROUTER_API_KEY : SecretStr = SecretStr("")
    OPENROUTER_URL     : str       = ""

    OPENAI_API_KEY     : SecretStr = SecretStr("")

    MAX_EXECUTION_TIMEOUT : int = 1800

    ACCESS_TOKEN_EXPIRE_SECONDS     : int = 900
    REFRESH_TOKEN_EXPIRE_SECONDS    : int = 7*24*3600


    model_config = SettingsConfigDict(
        env_file = ".env",
        extra    = "ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() 