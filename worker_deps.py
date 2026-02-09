import aiohttp

from repositories.price_repository import PriceRepository
from services.deribit_client import DeribitClient
from services.price_service import PriceService
from database.db import async_session
from contextlib import asynccontextmanager


@asynccontextmanager
async def price_service_ctx():
    session = async_session()
    try:
        repo = PriceRepository(session)
        deribit = DeribitClient(aiohttp.ClientSession())
        service = PriceService(repo, deribit)
        yield service
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
        await deribit.session.close()
