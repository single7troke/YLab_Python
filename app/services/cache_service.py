from fastapi import Depends
from repositories.cache_repository import CacheRepository


class CacheService:
    def __init__(self, cache: CacheRepository = Depends(CacheRepository)):
        self.cache = cache

    async def load_to_cache(self, key: str, value) -> bool:
        res = await self.cache.set(key=key, value=value)
        return res

    async def get_from_cache(self, key: str) -> bytes:
        data = await self.cache.get(key=key)
        return data

    async def menu_cache_invalidation(self, menu_id: str | None = None) -> None:
        await self.cache.delete(key='menu-list')
        if menu_id:
            await self.cache.delete(key=str(menu_id))

    async def submenu_cache_invalidation(self,
                                         menu_id: str,
                                         submenu_id: str | None = None) -> None:
        await self.menu_cache_invalidation(menu_id=menu_id)
        await self.cache.delete(key=f'{menu_id}-submenu-list')
        if submenu_id:
            await self.cache.delete(key=str(submenu_id))

    async def dish_cache_invalidation(self,
                                      menu_id: str,
                                      submenu_id: str,
                                      dish_id: str | None = None) -> None:
        await self.submenu_cache_invalidation(menu_id=menu_id, submenu_id=submenu_id)
        await self.cache.delete(key=f'{submenu_id}-dish-list')
        if dish_id:
            await self.cache.delete(key=str(dish_id))
