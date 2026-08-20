from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    APP_NAME       : str = "ExperimentOS"
    APP_VERSION    : str = "1.0.0"

    USER_NAME      : str = ""

    POSTGRES_URL   : str = ""
    REDIS_URL      : str = ""

    JWT_SECRET_KEY : str = ""
    JWT_ALGORITHM  : str = ""
    JWT_ISSUER     : str = ""
    JWT_AUDIENCE   : str = ""
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES : int = 0


    model_config = SettingsConfigDict(
        env_file = ".env",
        extra    = "ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() 