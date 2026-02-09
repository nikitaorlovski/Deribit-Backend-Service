from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer

from database.db import Base


class Price(Base):
    __tablename__ = "prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    price: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[int] = mapped_column(Integer, index=True)
