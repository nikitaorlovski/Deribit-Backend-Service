import aiohttp
import time

from fastapi import Request
from domain.models import PriceSnapshot


class DeribitClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_price(self, ticker: str) -> PriceSnapshot:
        try:
            async with self.session.get(
                f"https://test.deribit.com/api/v2/public/get_index_price",
                params={"index_name": ticker},
            ) as response:
                response.raise_for_status()
                price = await response.json()
                return PriceSnapshot(
                    ticker=ticker,
                    price=price["result"]["index_price"],
                    timestamp=time.time(),
                )
        except Exception as e:
            print("ERROR:", e)
            raise


async def get_deribit_client(request: Request) -> DeribitClient:
    return DeribitClient(request.app.state.http_session)
