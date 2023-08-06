import pickle
from uuid import UUID

from db.filters import GetAllDishesFilter, GetSingleDishFilter
from db.repositories import DishRepository
from fastapi import Depends, HTTPException
from schemas import CreateDish, Dish
from services import CacheService


class DishService:
    def __init__(self,
                 repository: DishRepository = Depends(DishRepository),
                 cache: CacheService = Depends(CacheService)):
        self.repository = repository
        self.cache = cache

    async def get(self, dish_id: UUID) -> Dish:
        data_from_cache = await self.cache.get_from_cache(key=str(dish_id))
        if data_from_cache:
            return Dish(**pickle.loads(data_from_cache))

        rows = await self.repository.get(custom_filter=GetSingleDishFilter(_id=dish_id))
        if rows:
            dish = Dish.fill(rows[0])
            await self.cache.load_to_cache(key=str(dish_id), value=pickle.dumps(dict(dish)))
            return dish
        raise HTTPException(status_code=404, detail='dish not found')

    async def list(self, submenu_id: UUID) -> list[Dish]:
        data_from_cache = await self.cache.get_from_cache(key=f'{submenu_id}-dish-list')
        if data_from_cache:
            dishes = [Dish(**submenu) for submenu in pickle.loads(data_from_cache)]
            return dishes
        rows = await self.repository.get(custom_filter=GetAllDishesFilter(_id=submenu_id))
        dishes = [Dish.fill(data=row) for row in rows]
        await self.cache.load_to_cache(
            key=f'{submenu_id}-dish-list',
            value=pickle.dumps([dict(submenu) for submenu in dishes]))
        return dishes

    async def create(self, menu_id: UUID, submenu_id: UUID, data: CreateDish) -> Dish | None:
        row = await self.repository.create(submenu_id=submenu_id, data=data)
        if row:
            await self.cache.dish_cache_invalidation(menu_id=str(menu_id), submenu_id=str(submenu_id))
            return Dish.fill(data=row)
        return None

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: CreateDish) -> Dish:
        rows = await self.repository.update(dish_id=dish_id, data=data)
        if rows:
            await self.cache.dish_cache_invalidation(
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
                dish_id=str(dish_id)
            )
            return Dish.fill(rows[0])
        else:
            raise HTTPException(status_code=404, detail='submenu not found')

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> dict | None:
        data = await self.repository.delete(dish_id=dish_id)
        if data:
            await self.cache.dish_cache_invalidation(
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
                dish_id=str(dish_id)
            )
            return {'status': True,
                    'message': 'The dish has been deleted'}
        return None
