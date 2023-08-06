from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class CreateMenu(BaseModel):
    title: str
    description: str


class CreateDish(CreateMenu):
    price: str


class Base(BaseOrJSONModel):
    id: UUID
    title: str
    description: str


class Menu(Base):
    submenus_count: int = 0
    dishes_count: int = 0

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   submenus_count=data.submenus_count,
                   dishes_count=data.dishes_count)


class SubMenu(Base):
    dishes_count: int = 0

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   dishes_count=data.dishes_count)


class Dish(Base):
    price: str

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   price=str(data.price))
