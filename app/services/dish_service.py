from uuid import UUID

from fastapi import Depends, HTTPException

from db.filters import GetSingleDishFilter, GetAllDishesFilter
from db.repositories import DishRepository
from schemas.schemas import Dish, CreateDish


class DishService:
    def __init__(self, repository: DishRepository = Depends(DishRepository)):
        self.repository = repository

    async def get(self, dish_id: UUID) -> Dish:
        rows = await self.repository.get(custom_filter=GetSingleDishFilter(_id=dish_id))
        if rows:
            row = rows[0]
            return Dish(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        price=str(row.price))
        raise HTTPException(status_code=404, detail="dish not found")

    async def list(self, submenu_id: UUID) -> list[Dish]:
        rows = await self.repository.get(custom_filter=GetAllDishesFilter(_id=submenu_id))
        for row in rows:
            pass

        return [Dish(id=str(row.id),
                     title=row.title,
                     description=row.description,
                     price=str(row.price)) for row in rows]

    async def create(self, submenu_id: UUID, data: CreateDish) -> Dish:
        row = await self.repository.create(submenu_id=submenu_id, data=data)
        if row:
            return Dish(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        price=str(row.price))

    async def update(self, dish_id: UUID, data: CreateDish) -> Dish:
        rows = await self.repository.update(dish_id=dish_id, data=data)
        if rows:
            row = rows[0]
            return Dish(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        price=str(row.price))
        raise HTTPException(status_code=404, detail="submenu not found")

    async def delete(self, dish_id: UUID) -> dict:
        data = await self.repository.delete(dish_id=dish_id)
        if data:
            return {"status": True,
                    "message": "The dish has been deleted"}
