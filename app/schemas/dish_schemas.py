from schemas.base_schema import Base
from schemas.menu_schemas import CreateMenu


class CreateDish(CreateMenu):
    price: str


class Dish(Base):
    price: str

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   price=str(data.price))
