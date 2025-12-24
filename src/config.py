from pydantic import BaseSettings


class Settings(BaseSettings):
    timeout_seconds: float = 5.0

    class Config:
        env_prefix = "APP_"


settings = Settings()