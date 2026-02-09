from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI
from api.routes import router as price_router
from redis.asyncio import Redis as aioredis
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
    )
    app.state.http_session = aiohttp.ClientSession()
    yield
    await app.state.http_session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(price_router)
