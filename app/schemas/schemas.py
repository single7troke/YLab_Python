import orjson
from uuid import UUID

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Test(BaseModel):
    title: str
    description: str


class Base(BaseOrJSONModel):
    id: UUID
    title: str
    description: str


class Menu(Base):
    submenus_count: int
    dishes_count: int


class SubMenu(Base):
    dishes_count: int


class Dish(Base):
    price: str
