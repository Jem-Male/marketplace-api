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
    
    model: Type[ModelType]
    
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    async def get_by_id(
        cls, 
        session: AsyncSession, 
        record_id: Any, 
        is_active: bool | None = None
    ) -> Optional[ModelType]:
        query = select(cls.model).where(cls.model.id == record_id)
        
        if is_active is not None:
            query = query.where(cls.model.is_active==is_active)
        
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def get_all(
        cls, 
        session: AsyncSession, 
        skip: int=0, 
        limit: int=100,
        is_active: bool | None = None
    ) -> List[ModelType]:
        query = select(cls.model)
        if is_active is not None:
            query = query.where(cls.model.is_active==is_active)
        result = await session.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()


    @classmethod
    async def create(cls, session: AsyncSession, schema: CreateSchemaType) -> ModelType:
        db_obj = cls.model(**schema.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


    @classmethod
    async def update(cls, session: AsyncSession, record_id: Any, schema: UpdateSchemaType) -> Optional[ModelType]:
        update_dict = schema.model_dump(exclude_unset=True)
        stmt = update(cls.model).where(cls.model.id == record_id).values(**update_dict)
        await session.execute(stmt)
        await session.commit()
        return await cls.get_by_id(session, record_id)


    @classmethod
    async def delete(cls, session: AsyncSession, record_id: Any) -> bool:
        stmt = delete(cls.model).where(cls.model.id == record_id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0