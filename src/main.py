from contextlib import asynccontextmanager

from fastapi import Body, FastAPI, Path, Query, status
from telegram import Update

from src.bot import telegram_app
from src.config import settings
from src.logger import logger, setup_logging
from src.schemas import WebhookData


setup_logging()


@asynccontextmanager
async def lifespan(_):
    await telegram_app.bot.set_webhook(
        settings.TELEGRAM_WEBHOOK_URL.encoded_string(),
        allowed_updates=Update.ALL_TYPES,
    )
    async with telegram_app:
        await telegram_app.start()
        yield
        await telegram_app.stop()


app = FastAPI(
    title='FastAPI PTB',
    lifespan=lifespan,
    root_path='/telegram',
)


@app.post(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    include_in_schema=False,
)
async def telegram(body=Body()) -> None:
    """接收 Telegram Webhook 发来的数据，将其转换成机器人程序可识别的内容"""

    await logger.adebug('Receive telegram data')
    update = Update.de_json(data=body, bot=telegram_app.bot)
    await telegram_app.update_queue.put(update)


@app.get('/health-check', status_code=status.HTTP_204_NO_CONTENT)
async def health_check(): ...


@app.get(
    '/{chat_id}/users/{user_id}',
    status_code=status.HTTP_202_ACCEPTED,
)
async def push(
    chat_id: int = Path(),
    user_id: int = Path(),
    notify: bool = Query(False),
    value: list[str] = Query(default_factory=list),
) -> None:
    data = WebhookData(
        user_id=user_id,
        chat_id=chat_id,
        value=value,
        notify=notify,
    )
    await telegram_app.update_queue.put(data)
