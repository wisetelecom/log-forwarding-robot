from pydantic import BaseModel


class WebhookUpdate(BaseModel):
    """Simple dataclass to wrap a custom update type"""

    user_id: int
    payloads: list[str]
