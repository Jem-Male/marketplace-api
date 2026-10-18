from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Enum as SqlEnum,
    func
    )
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    MANAGER = "manager"
    OWNER = "owner"
    ADMIN = "admin"


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email : Mapped[str] = mapped_column(String(200), nullable=False)
    number: Mapped[str] = mapped_column(String(25), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, values_callable=lambda obj: [e.value for e in obj]), 
        default=UserRole.CUSTOMER, 
        server_default="customer"
    )

    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    
    default_delivery_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
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