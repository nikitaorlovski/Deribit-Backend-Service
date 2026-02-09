from dataclasses import dataclass


@dataclass(frozen=True)
class PriceSnapshot:
    ticker: str
    price: float
    timestamp: float
