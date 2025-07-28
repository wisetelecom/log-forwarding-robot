import logging
import logging.config

import structlog

from src.config import settings


# 公用处理链
shared_processors = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(fmt='iso'),
]


def extract_environment(
    _,
    log_level: str,  # noqa: ARG001
    event_dict,
):
    """
    提取环境信息
    """
    record: logging.LogRecord = event_dict['_record']

    event_dict['thread_name'] = record.threadName
    event_dict['process_name'] = record.processName
    event_dict['target'] = f'{record.pathname}:{record.lineno}'
    return event_dict


handlers = ['console']


CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': handlers,
        'level': settings.LOG_LEVEL,
    },
    'formatters': {
        'colored': {
            '()': structlog.stdlib.ProcessorFormatter,
            'foreign_pre_chain': shared_processors,
            'processors': [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
        },
    },
    'handlers': {
        'console': {
            '()': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        '()': {
            'handlers': handlers,
            'level': settings.LOG_LEVEL,
            'propagate': True,
        },
        'uvicorn': {
            'propagate': True,
        },
        'watchfiles': {
            'propagate': True,
            'level': 'ERROR',
        },
        'multipart.multipart': {
            'propagate': True,
            'level': 'ERROR',
        },
        'fastapi': {
            'propagate': True,
        },
        'httpx': {
            'propagate': True,
        },
        'httpcore': {
            'propagate': True,
        },
        'telegram': {
            'propagate': True,
        },
    },
}


def setup_logging():
    """
    配置整个应用的日志系统
    """

    logging.config.dictConfig(CONFIG)

    structlog.configure(
        processors=[
            *shared_processors,
            # If some value is in bytes, decode it to a Unicode str.
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


logger = get_logger('ptb')
