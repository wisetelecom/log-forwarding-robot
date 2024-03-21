import datetime
import logging
import sys

from loguru import logger

from src.config import settings


logger.remove()


# line 8-26 ref: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 0
        while frame and (
            depth == 0 or frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


# line 29-31 ref: https://medium.com/1mgofficial/how-to-override-uvicorn-logger-in-fastapi-using-loguru-124133cdcd4e
for _log in ['uvicorn', 'uvicorn.error', 'uvicorn.access', 'fastapi']:
    _logger = logging.getLogger(_log)
    _logger.handlers = [InterceptHandler()]

logging.getLogger('httpx').setLevel('WARNING')

LOG_FORMAT = (
    '<level>{level: <8}</level> | '
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
    '<cyan>{name}</cyan>:'
    '<cyan>{function}</cyan>:'
    '<cyan>{line}</cyan> - '
    '<level>{message}</level>'
)

logger.add(sys.stdout, format=LOG_FORMAT)


class Rotator:
    """指定大小和时间更新日志文件"""

    def __init__(self, *, size):
        now = datetime.datetime.now()

        self._size_limit = size
        # 每晚 0 点更新
        self._time_limit = now.replace(hour=0, minute=0, second=0)
        if now >= self._time_limit:
            # The current time is already past the target time so it would
            # rotate already. Add one day to prevent an immediate rotation.
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True

        excess = (
            message.record['time'].timestamp() - self._time_limit.timestamp()
        )
        if excess >= 0:
            elapsed_days = datetime.timedelta(seconds=excess).days
            self._time_limit += datetime.timedelta(days=elapsed_days + 1)
            return True
        return False


if not settings.DEBUG:
    # 20MB
    rotator = Rotator(size=2e7)
    logger.add(
        './log/run.log',
        level='INFO',
        format=LOG_FORMAT,
        rotation=rotator.should_rotate,
    )
