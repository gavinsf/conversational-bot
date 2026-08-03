from fastapi import FastAPI
from back.chat import router as chat_router
from contextlib import asynccontextmanager

from back.dynamo import close_table


async def lifespan(app: FastAPI):
    yield
    await close_table()


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router, prefix="/api")