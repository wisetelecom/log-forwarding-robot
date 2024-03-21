from typing import TypeVar

from telegram.ext import Application, CommandHandler, TypeHandler

from src.ptb.handlers import start, webhook_update
from src.ptb.models import WebhookUpdate


_AppT = TypeVar('_AppT', bound=Application)


def setup_ptb(tgbot: _AppT) -> _AppT:
    # register handlers
    tgbot.add_handler(CommandHandler('start', start))
    tgbot.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))

    return tgbot
