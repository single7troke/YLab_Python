from pydantic import Field
from schemas.base_schema import Base, BaseOrJSONModel


class CreateMenu(BaseOrJSONModel):
    title: str = Field(examples=['My menu'])
    description: str = Field(examples=['My menu description'])


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
