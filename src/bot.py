from telegram.ext import Application, ContextTypes

from .config import settings
from .context import WebhookDataContext
from .handlers import handlers


ctx_type = ContextTypes(context=WebhookDataContext)

telegram_app = (
    Application.builder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .context_types(ctx_type)
    .updater(None)
    .build()
)
telegram_app.add_handlers(handlers)
