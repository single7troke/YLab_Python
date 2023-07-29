from pydantic import BaseModel


class Response(BaseModel):
    data: dict | list
    status_code: int
    headers: dict


class BaseMenu(BaseModel):
    id: str
    title: str
    description: str


class Menu(BaseMenu):
    submenus_count: int
    dishes_count: int


class SubMenu(BaseMenu):
    dishes_count: int


class Dish(BaseMenu):
    price: str
