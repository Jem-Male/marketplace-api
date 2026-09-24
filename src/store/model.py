from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func, Boolean, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TaxRegime(str, Enum):
    SIMPLIFIED = "simplified"
    COMMON = "common"
    PATENT = "patent"


class StoreModel(Base):
    __tablename__ = "stores"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    image: Mapped[str | None] = mapped_column(String(2048), nullable=True)    
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bin_iin: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    legal_address: Mapped[str] = mapped_column(String(500), nullable=False)
    tax_regime: Mapped[TaxRegime] = mapped_column(SqlEnum(TaxRegime), nullable=False)
    license_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bank_account: Mapped[str] = mapped_column(String(34), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bik: Mapped[str] = mapped_column(String(11), nullable=False)
    physical_address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    kkm_serial_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ofd_token: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )