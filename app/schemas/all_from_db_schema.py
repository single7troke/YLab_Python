from schemas import Dish
from schemas.base_schema import Base


class SubMenuWithDishes(Base):
    dishes: list[Dish]

    @classmethod
    def fill(cls, sub):
        return cls(id=sub.id,
                   title=sub.title,
                   description=sub.description,
                   dishes=[Dish.fill(dish) for dish in sub.dishes])


class Everything(Base):
    submenus: list[SubMenuWithDishes]

    @classmethod
    def fill(cls, menu):
        return cls(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus=[SubMenuWithDishes.fill(sub) for sub in menu.submenus])
