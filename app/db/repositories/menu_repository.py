import uuid
from typing import Sequence

from fastapi import Depends
from sqlalchemy import select, insert, update, delete, func, distinct, Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.filters import Specification, GetSingleMenuFilter
from db.models import Menu, SubMenu, Dish
from db.pg_db import get_session


class MenuRepository:

    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db
        self.model = Menu

    async def get(self, custom_filter: Specification) -> Sequence[Row]:
        try:
            data = await self.db.execute(
                select(
                    Menu.id,
                    Menu.title,
                    Menu.description,
                    func.count(distinct(SubMenu.id)).label("submenus_count"),
                    func.count(distinct(Dish.id)).label("dishes_count")
                )
                .filter_by(**custom_filter.is_satisfied())
                .outerjoin(SubMenu, Menu.id == SubMenu.menu_id)
                .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
                .group_by(Menu.id)
            )
            return data.all()
        except Exception as e:
            raise e

    async def create(self, data) -> Row:
        _id = uuid.uuid4()
        try:
            data = await self.db.execute(
                insert(self.model).values(id=_id, **dict(data)).returning(self.model))
            row = data.scalars().one()
            await self.db.commit()
            return row
        except Exception as e:
            raise e

    async def update(self, menu_id, data) -> Sequence[Row] | None:
        try:
            await self.db.execute(
                update(self.model).where(self.model.id == menu_id).values(**dict(data)).returning(self.model))
            await self.db.commit()
            row = await self.get(custom_filter=GetSingleMenuFilter(_id=menu_id))
            return row
        except NoResultFound:
            return None

    async def delete(self, menu_id):
        try:
            await self.db.execute(delete(self.model).where(self.model.id == menu_id))
            await self.db.commit()
            return 1
        except Exception as e:
            raise e
