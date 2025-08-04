from telegram.ext import Application, CallbackContext, ExtBot

from .schemas import WebhookData


class WebhookDataContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates
    of type `WebhookData`.
    """

    @classmethod
    def from_update(
        cls,
        update,
        application: Application,
    ) -> 'WebhookDataContext':
        if isinstance(update, WebhookData):
            return cls(
                application=application,
                chat_id=update.chat_id,
                user_id=update.user_id,
            )

        return super().from_update(update, application)
