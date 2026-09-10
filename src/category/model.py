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

from typing import Optional
from datetime import datetime


class CategoryModel(Base):
    __tablename__ = "categoryes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100),unique=True , nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    
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