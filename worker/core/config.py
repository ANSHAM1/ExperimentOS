from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    APP_NAME         : str = "ExperimentOS-Worker"
    APP_VERSION      : str = "1.0.0"

    POSTGRES_URL     : str = ""
    REDIS_URL        : str = ""
    RABBITMQ_URL     : str = ""

    EXPERIMENT_QUEUE : str = "experiment_queue"

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra    = "ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() 