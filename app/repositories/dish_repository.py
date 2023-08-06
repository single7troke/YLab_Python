from typing import Sequence
from uuid import UUID, uuid4

from db.filters import GetSingleDishFilter, Specification
from db.models import Dish
from db.pg_db import get_session
from fastapi import Depends
from schemas import CreateDish
from sqlalchemy import Row, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.db = session
        self.model = Dish

    async def get(self, custom_filter: Specification) -> Sequence[Dish]:
        data = await self.db.execute(
            select(self.model).
            filter_by(**custom_filter.is_satisfied())
        )
        return data.scalars().all()

    async def create(self, submenu_id: UUID, data: CreateDish) -> Row:
        _id = uuid4()
        data = await self.db.execute(
            insert(self.model)
            .values(id=_id, submenu_id=submenu_id, **dict(data))
            .returning(self.model)
        )
        row = data.scalars().one()
        await self.db.commit()
        return row

    async def update(self, dish_id: UUID, data) -> Sequence[Dish] | None:
        await self.db.execute(
            update(self.model)
            .where(self.model.id == dish_id)
            .values(**dict(data)).returning(self.model)
        )
        await self.db.commit()
        row = await self.get(custom_filter=GetSingleDishFilter(_id=dish_id))
        return row

    async def delete(self, dish_id: UUID) -> bool:
        await self.db.execute(
            delete(self.model).where(self.model.id == dish_id)
        )
        await self.db.commit()
        return True
