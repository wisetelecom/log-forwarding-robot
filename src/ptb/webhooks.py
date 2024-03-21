from fastapi import APIRouter, Query, Request
from telegram import Update

from src.ptb import tgbot
from src.ptb.models import WebhookUpdate


webhooks = APIRouter(tags=['PTB Webhooks'])


@webhooks.post('/telegram', response_model=None)
async def telegram(request: Request):
    """Handle incoming Telegram updates by putting them into the
    `update_queue`"""

    await tgbot.update_queue.put(
        Update.de_json(data=await request.json(), bot=tgbot.bot)
    )


@webhooks.get('/submitpayload', response_model=str)
@webhooks.post('/submitpayload', response_model=str)
async def custom_updates(
    user_id: int = Query(), payload: list[str] = Query()
) -> str:
    """
    Handle incoming webhook updates by also putting them into the
    `update_queue` if the required parameters were passed correctly.
    """

    await tgbot.update_queue.put(
        WebhookUpdate(user_id=user_id, payloads=payload)
    )
    return "Thank you for the submission! It's being forwarded."


@webhooks.get('/healthcheck', response_model=str)
async def health() -> str:
    """For the health endpoint, reply with a simple plain text message."""

    return 'The bot is still running fine :)'
