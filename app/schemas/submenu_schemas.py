from schemas.base_schema import Base
from schemas.menu_schemas import CreateMenu


class CreateSubmenu(CreateMenu):
    pass


class SubMenu(Base):
    dishes_count: int = 0

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   dishes_count=data.dishes_count)
