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


    async def get_by_id(
        self, 
        record_id: Any, 
        is_active: bool | None = None
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == record_id)
        
        if is_active is not None:
            query = query.where(self.model.is_active==is_active)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def get_all(
        self, 
        skip: int=0, 
        limit: int=10000,
        is_active: bool | None = None
    ) -> List[ModelType]:
        query = select(self.model)
        
        if is_active is not None:
            query = query.where(self.model.is_active==is_active)
            
        result = await self.session.execute(
            query.offset(skip).limit(limit)
        )
        
        return result.scalars().all()


    async def create(self, schema: CreateSchemaType) -> ModelType:
        db_obj = self.model(**schema.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj


    async def update(self, record_id: Any, schema: UpdateSchemaType) -> Optional[ModelType]:
        update_dict = schema.model_dump(exclude_unset=True)
        stmt = update(self.model).where(self.model.id == record_id).values(**update_dict)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_by_id(record_id)


    async def delete(self, record_id: Any) -> bool:
        stmt = delete(self.model).where(self.model.id == record_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0