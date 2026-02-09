import time
import datetime
import pytest
from database.models.price import Price


async def generate_prices(session):
    now = int(time.time())
    prices = [
        Price(ticker="eth_usd", price=91000, timestamp=now),
        Price(ticker="btc_usd", price=93000, timestamp=now - 100),
        Price(ticker="eth_usd", price=90000, timestamp=now - 1000),
    ]
    session.add_all(prices)
    await session.commit()


@pytest.mark.asyncio
async def test_get_prices(client, db_session):
    await generate_prices(db_session)

    resp = await client.get("/prices/", params={"ticker": "eth_usd"})
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 2
    assert all(item["ticker"] == "eth_usd" for item in data)


@pytest.mark.asyncio
async def test_get_last_price(client, db_session):
    await generate_prices(db_session)
    resp = await client.get("/prices/latest", params={"ticker": "eth_usd"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "eth_usd"
    assert data["price"] == 91000


@pytest.mark.asyncio
async def test_get_last_price_by_date(client, db_session):
    await generate_prices(db_session)
    now = datetime.date.today()
    resp = await client.get("/prices/latest", params={"ticker": "btc_usd", "at": now})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "btc_usd"
    assert data["price"] == 93000
