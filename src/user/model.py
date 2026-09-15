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

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email : Mapped[str] = mapped_column(String(200), nullable=False)
    number: Mapped[str] = mapped_column(String(15), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
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
    

# from datetime import datetime
# from enum import Enum
# from typing import Optional
# from sqlalchemy import String, DateTime, func, Boolean, Enum as SqlEnum
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# class UserRole(str, Enum):
#     CUSTOMER = "customer"    # Покупатель
#     MANAGER = "manager"      # Менеджер магазина / Продавец
#     OWNER = "owner"          # Владелец магазина (партнер)
#     ADMIN = "admin"          # Администратор всей платформы

# class UserModel(Base):
#     __tablename__ = "users"
    
#     # --- Базовая информация ---
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)  # Имя / ФИО
#     email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False) # Уникальный email
#     number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False) # Номер телефона (сделан уникальным)
#     hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
#     description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
#     image: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    
#     # --- Роли и Права ---
#     role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.CUSTOMER, server_default="customer")
    
#     # --- Статусы верификации ---
#     is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
#     is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    
#     # --- Дополнительные данные (для доставки) ---
#     default_delivery_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
#     # --- Системные поля ---
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), 
#         server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), 
#         server_default=func.now(), 
#         onupdate=func.now()
#     )
