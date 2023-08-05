from typing import Sequence
from uuid import uuid4, UUID
from fastapi import Depends
from sqlalchemy import select, insert, update, delete, Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.filters import Specification, GetSingleDishFilter
from db.models import Dish
from db.pg_db import get_session
from schemas.schemas import CreateDish


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.db = session
        self.model = Dish

    async def get(self, custom_filter: Specification) -> Sequence[Dish]:
        try:
            data = await self.db.execute(
                select(self.model).
                filter_by(**custom_filter.is_satisfied())
            )
            return data.scalars().all()
        except Exception as e:
            raise e

    async def create(self, submenu_id: UUID, data: CreateDish) -> Row:
        _id = uuid4()
        try:
            data = await self.db.execute(
                insert(self.model)
                .values(id=_id, submenu_id=submenu_id, **dict(data))
                .returning(self.model)
            )
            row = data.scalars().one()
            await self.db.commit()
            return row
        except Exception as e:
            raise e

    async def update(self, dish_id: UUID, data: CreateDish) -> Sequence[Dish] | None:
        try:
            await self.db.execute(
                update(self.model)
                .where(self.model.id == dish_id)
                .values(**dict(data)).returning(self.model)
            )
            await self.db.commit()
            data = await self.get(custom_filter=GetSingleDishFilter(_id=dish_id))
            return data
        except NoResultFound:
            return None

    async def delete(self, dish_id: UUID) -> bool:
        try:
            await self.db.execute(
                delete(self.model).where(self.model.id == dish_id)
            )
            await self.db.commit()
            return True
        except NoResultFound:
            return False
