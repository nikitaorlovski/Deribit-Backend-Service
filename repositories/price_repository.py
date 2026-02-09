from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from database.models.price import Price


class PriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_prices_by_ticker(self, ticker: str) -> list[Price]:
        result = await self.session.execute(select(Price).where(Price.ticker == ticker))
        return result.scalars().all()

    async def get_last_price(self, ticker: str) -> Price | None:
        result = await self.session.execute(
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_price_by_date(self, ticker: str, date: int) -> Price | None:
        result = await self.session.execute(
            select(Price)
            .where(Price.ticker == ticker, Price.timestamp <= date)
            .order_by(Price.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def add_new_price(self, price: Price):
        self.session.add(price)


async def get_price_repository(session: AsyncSession = Depends(get_session)):
    return PriceRepository(session=session)
