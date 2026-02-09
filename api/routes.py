from typing import Literal

from fastapi import Depends, APIRouter
from fastapi.params import Query
from fastapi import HTTPException
from datetime import date
from domain.exceptions import PriceNotFound
from schemas.price import PriceOut
from services.price_service import PriceService, get_price_service

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/", response_model=list[PriceOut])
async def get_prices(
    ticker: Literal["eth_usd", "btc_usd"] = Query(...),
    service: PriceService = Depends(get_price_service),
):
    try:
        prices = await service.get_all_prices(ticker=ticker)
    except PriceNotFound:
        raise HTTPException(status_code=404, detail="Prices not found")
    return prices


@router.get("/latest", response_model=PriceOut)
async def get_latest_price(
    ticker: Literal["eth_usd", "btc_usd"] = Query(...),
    at: date | None = Query(None, description="YYYY-MM-DD"),
    service: PriceService = Depends(get_price_service),
):
    try:
        price = (
            await service.get_last_price(ticker=ticker)
            if at is None
            else await service.get_price_by_date(ticker=ticker, at=at)
        )
    except PriceNotFound:
        raise HTTPException(status_code=404, detail="Price not found")

    return price
