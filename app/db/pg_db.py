import uuid

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import Config
from db.abstract_db import AbstractDB
from db.models import Menu, SubMenu, Dish

config = Config()

DATABASE_URL = config.postgres.url()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class PostgresDB(AbstractDB):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, _id: str, model):
        data = await self.session.execute(select(model).where(model.id == _id))
        return data.scalar()

    async def get_all(self, model, **kwargs):
        if model == SubMenu:
            data = await self.session.execute(select(model).where(model.menu_id == kwargs["_id"]))
            return data.scalars().all()
        elif model == Dish:
            data = await self.session.execute(select(model).where(model.submenu_id == kwargs["_id"]))
            return data.scalars().all()
        data = await self.session.execute(select(model))
        return data.scalars().all()

    async def create(self, model, **kwargs):
        _id = uuid.uuid4()
        try:
            if model is Menu:
                await self.session.execute(insert(model).values(id=_id, **kwargs))

            if model is SubMenu:
                await self.session.execute(insert(model).values(id=_id, **kwargs))
                menu_id = kwargs["menu_id"]
                row = await self.get_one(_id=menu_id, model=Menu)
                new_count = row.submenu_counter + 1
                await self.update(_id=menu_id, model=Menu, data={"submenu_counter": new_count})

            if model is Dish:
                data = {k: v for k, v in kwargs.items() if k != "menu_id"}
                await self.session.execute(insert(model).values(id=_id, **data))
                menu_id = kwargs["menu_id"]
                submenu_id = kwargs["submenu_id"]
                menu = await self.get_one(_id=menu_id, model=Menu)
                submenu = await self.get_one(_id=submenu_id, model=SubMenu)
                menu_dish_count = menu.dish_counter + 1
                submenu_dish_count = submenu.dish_counter + 1
                await self.update(_id=menu_id, model=Menu, data={"dish_counter": menu_dish_count})
                await self.update(_id=submenu_id, model=SubMenu, data={"dish_counter": submenu_dish_count})

            await self.session.commit()
            data = await self.get_one(_id=str(_id), model=model)
            return data
        except Exception as e:
            raise e

    async def update(self, _id, model, data):
        try:
            await self.session.execute(update(model).where(model.id == _id).values(**dict(data)))
            await self.session.commit()
            data = await self.get_one(_id=str(_id), model=model)
            return data
        except Exception as e:
            raise e

    async def delete(self, _id, model):
        try:
            if model is SubMenu:
                submenu = await self.get_one(_id=_id, model=model)
                submenu_dish_count = submenu.dish_counter
                menu_id = submenu.menu_id

                menu = await self.get_one(_id=menu_id, model=Menu)
                menu_dish_count = menu.dish_counter - submenu_dish_count
                submenu_count = menu.submenu_counter - 1

                await self.update(_id=menu_id,
                                  model=Menu,
                                  data={"submenu_counter": submenu_count,
                                        "dish_counter": menu_dish_count})

            elif model is Dish:
                dish = await self.get_one(_id=_id, model=Dish)
                submenu_id = dish.submenu_id
                submenu = await self.get_one(_id=submenu_id, model=SubMenu)
                menu_id = submenu.menu_id
                menu = await self.get_one(_id=menu_id, model=Menu)
                menu_dish_count = menu.dish_counter - 1
                submenu_dish_count = submenu.dish_counter - 1
                await self.update(_id=menu_id, model=Menu, data={"dish_counter": menu_dish_count})
                await self.update(_id=submenu_id, model=SubMenu, data={"dish_counter": submenu_dish_count})

            await self.session.execute(delete(model).where(model.id == _id))
            await self.session.commit()
            return 1
        except Exception as e:
            raise e
