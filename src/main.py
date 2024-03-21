from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.logger import logger  # noqa: F401
from src.ptb import tgbot
from src.router import router


@asynccontextmanager
async def lifespan(_):
    async with tgbot:
        await tgbot.start()
        yield
        await tgbot.stop()


app = FastAPI(title='FastAPI PTB', lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)
