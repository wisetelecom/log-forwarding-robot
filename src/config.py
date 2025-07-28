from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import LogLevel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='FASTAPI_',
        env_file=('.env', '.env.local', '.env.dev', '.env.prod'),
        env_file_encoding='utf-8',
        env_nested_delimiter='_',
        extra='ignore',
    )

    LOG_LEVEL: LogLevel = LogLevel.INFO

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_WEBHOOK_URL: HttpUrl


settings = Settings()  # type: ignore
