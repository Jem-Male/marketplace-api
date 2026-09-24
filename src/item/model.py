from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    ForeignKey,
    CheckConstraint,
    DateTime,
    func
)

from decimal import Decimal
from typing import Optional
from datetime import datetime


class ItemModel(Base):
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    category: Mapped[int | None] = mapped_column(ForeignKey("categoryes.id", ondelete="RESTRICT"), nullable=True)
    creator: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    store: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    is_active: Mapped[bool] = mapped_column(default=True)
    stock: Mapped[int] = mapped_column(
        CheckConstraint("stock >= 0", name="check_stock_positive"),
        default=1
    )