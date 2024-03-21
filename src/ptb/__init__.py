from telegram.ext import Application, ContextTypes

from src.config import settings
from src.ptb.bot import setup_ptb
from src.ptb.utils import CustomContext


"""
Set up PTB application and a web application for handling the incoming
requests.
"""
context_types = ContextTypes(context=CustomContext)
# Here we set updater to None because we want our custom webhook server to
# handle the updates and hence we don't need an Updater instance
tgbot = setup_ptb(
    Application.builder()
    .token(settings.TELEGRAM_TOKEN)
    .updater(None)
    .context_types(context_types)
    .build()
)
