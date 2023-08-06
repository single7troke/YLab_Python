from pydantic import Field
from schemas.base_schema import Base, BaseOrJSONModel


class CreateDish(BaseOrJSONModel):
    title: str = Field(examples=['My dish'])
    description: str = Field(examples=['My dish description'])
    price: str = Field(examples=['12.50'])


class Dish(Base):
    price: str = Field(examples=['12.50'])

    @classmethod
    def fill(cls, data):
        return cls(id=str(data.id),
                   title=data.title,
                   description=data.description,
                   price=str(data.price))
