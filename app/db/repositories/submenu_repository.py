from uuid import uuid4, UUID
from typing import Sequence

from fastapi import Depends
from sqlalchemy import select, insert, update, delete, Row, func, distinct
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.filters import Specification, GetSingleSubmenuFilter
from db.models import SubMenu, Dish
from db.pg_db import get_session
from schemas import schemas


class SubmenuRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.db = session
        self.model = SubMenu

    async def get(self, custom_filter: Specification) -> Sequence[Row]:
        try:
            data = await self.db.execute(
                select(SubMenu.id,
                       SubMenu.title,
                       SubMenu.description,
                       func.count(distinct(Dish.id)).label("dishes_count")
                       )
                .filter_by(**custom_filter.is_satisfied())
                .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
                .group_by(SubMenu.id)
            )
            return data.all()
        except Exception as e:
            raise e

    async def create(self, menu_id: UUID, data: schemas.CreateMenu) -> Row:
        _id = uuid4()
        try:
            data = await self.db.execute(
                insert(self.model).values(id=_id, menu_id=menu_id, **dict(data)).returning(self.model))
            row = data.scalars().one()
            await self.db.commit()
            return row
        except Exception as e:
            raise e

    async def update(self, submenu_id: UUID, data: schemas.CreateMenu) -> Sequence[Row] | None:
        try:
            await self.db.execute(
                update(self.model)
                .where(self.model.id == submenu_id)
                .values(**dict(data))
            )
            await self.db.commit()
            row = await self.get(custom_filter=GetSingleSubmenuFilter(_id=submenu_id))
            return row
        except NoResultFound:
            return None

    async def delete(self, submenu_id: UUID) -> bool:
        try:
            await self.db.execute(delete(self.model).where(self.model.id == submenu_id))
            await self.db.commit()
            return True
        except Exception as e:
            raise e
