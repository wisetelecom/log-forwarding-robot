from pydantic import BaseModel


class WebhookData(BaseModel):
    user_id: int
    chat_id: int
    value: list[str]
