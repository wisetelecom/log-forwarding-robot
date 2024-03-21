import asyncio

from telegram import Update

from src.ptb import tgbot
from src.ptb.constants import WEBHOOK_URL


asyncio.run(
    tgbot.bot.set_webhook(
        url=f'{WEBHOOK_URL}/telegram',
        allowed_updates=Update.ALL_TYPES,
    )
)
