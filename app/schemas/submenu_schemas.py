from pydantic import Field
from schemas.base_schema import Base, BaseOrJSONModel


class CreateSubmenu(BaseOrJSONModel):
    title: str = Field(examples=['My submenu'])
    description: str = Field(examples=['My submenu description'])


class SubMenu(Base):
    dishes_count: int = 0

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   dishes_count=data.dishes_count)
