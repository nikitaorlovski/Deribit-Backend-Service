from fastapi import Depends

from database.models.price import Price
from domain.exceptions import PriceNotFound
from repositories.price_repository import PriceRepository, get_price_repository
from services.deribit_client import DeribitClient, get_deribit_client
from datetime import date, datetime, time


class PriceService:
    def __init__(self, repo: PriceRepository, deribit: DeribitClient):
        self.repo = repo
        self.deribit = deribit

    async def get_all_prices(self, ticker: str):
        prices = await self.repo.get_prices_by_ticker(ticker=ticker)
        if not prices:
            raise PriceNotFound
        return prices

    async def get_last_price(self, ticker: str):
        price = await self.repo.get_last_price(ticker=ticker)
        if not price:
            raise PriceNotFound
        return price

    async def get_price_by_date(self, ticker: str, at: date):
        dt = datetime.combine(at, time.max)
        timestamp = int(dt.timestamp())
        price = await self.repo.get_price_by_date(ticker=ticker, date=timestamp)
        if not price:
            raise PriceNotFound
        return price

    async def add_new_price(self, ticker: str):
        new_price = await self.deribit.fetch_price(ticker=ticker)
        await self.repo.add_new_price(
            price=Price(
                ticker=new_price.ticker,
                price=new_price.price,
                timestamp=int(new_price.timestamp),
            )
        )


async def get_price_service(
    repository: PriceRepository = Depends(get_price_repository),
    deribit: DeribitClient = Depends(get_deribit_client),
):
    return PriceService(repo=repository, deribit=deribit)
