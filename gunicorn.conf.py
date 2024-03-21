import multiprocessing
from enum import StrEnum, auto

from pydantic import Field, IPvAnyAddress, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class GunicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='GUNICORN_',
        env_file=('.env',),
        env_file_encoding='utf-8',
        extra='ignore',
    )

    RELOAD: bool = False
    HOST: IPvAnyAddress = '0.0.0.0'  # type: ignore
    PORT: PositiveInt = Field(80, le=65535)
    WORKERS_PER_CORE: int = 1
    WORKERS: PositiveInt = max(multiprocessing.cpu_count(), 2)

    LOG_LEVEL: LogLevel = LogLevel.INFO

    ACCESS_LOG: str = '-'
    ERROR_LOG: str = '-'

    GRACEFUL_TIMEOUT: PositiveInt = 120
    TIMEOUT: PositiveInt = 120
    KEEP_ALIVE: PositiveInt = 5


gunicorn_settings = GunicornSettings()  # type: ignore


# Gunicorn config variables
reload = gunicorn_settings.RELOAD
loglevel = gunicorn_settings.LOG_LEVEL
workers = gunicorn_settings.WORKERS
bind = f'{gunicorn_settings.HOST}:{gunicorn_settings.PORT}'
errorlog = gunicorn_settings.ERROR_LOG
worker_tmp_dir = '/dev/shm'
accesslog = gunicorn_settings.ACCESS_LOG
graceful_timeout = gunicorn_settings.GRACEFUL_TIMEOUT
timeout = gunicorn_settings.TIMEOUT
keepalive = gunicorn_settings.KEEP_ALIVE
