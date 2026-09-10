from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, record_id: Any) -> Optional[ModelType]:
        result = await session.execute(select(self.model).where(self.model.id == record_id))
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession, skip: int=0, limit: int=100) -> List[ModelType]:
        result = await session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, session: AsyncSession, schema: CreateSchemaType) -> ModelType:
        db_obj = self.model(**schema.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, session: AsyncSession, record_id: Any, schema: UpdateSchemaType) -> Optional[ModelType]:
        update_dict = schema.model_dump(exclude_unset=True)
        stmt = update(self.model).where(self.model.id == record_id).values(**update_dict)
        await session.execute(stmt)
        await session.commit()
        return await self.get_by_id(session, record_id)

    async def delete(self, session: AsyncSession, record_id: Any) -> bool:
        stmt = delete(self.model).where(self.model.id == record_id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0