from pydantic import BaseModel
from schemas.base_schema import Base


class CreateMenu(BaseModel):
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
