import pickle
from uuid import UUID

from db.filters import GetAllMenusFilter, GetSingleMenuFilter
from fastapi import Depends, HTTPException
from repositories.menu_repository import MenuRepository
from schemas import CreateMenu, Menu
from services import CacheService


class MenuService:
    def __init__(self,
                 repository: MenuRepository = Depends(MenuRepository),
                 cache: CacheService = Depends(CacheService)):
        self.repository = repository
        self.cache = cache

    async def get(self, menu_id: UUID) -> Menu:
        data_from_cache = await self.cache.get_from_cache(key=str(menu_id))
        if data_from_cache:
            return Menu(**pickle.loads(data_from_cache))
        rows = await self.repository.get(custom_filter=GetSingleMenuFilter(_id=menu_id))
        if rows:
            menu = Menu.fill(data=rows[0])
            await self.cache.load_to_cache(key=str(menu_id), value=pickle.dumps(dict(menu)))
            return menu
        raise HTTPException(status_code=404, detail='menu not found')

    async def list(self) -> list[Menu]:
        data_from_cache = await self.cache.get_from_cache(key='menu-list')
        if data_from_cache:
            return [Menu(**menu) for menu in pickle.loads(data_from_cache)]
        rows = await self.repository.get(custom_filter=GetAllMenusFilter())
        menus = [Menu.fill(data=i) for i in rows]
        await self.cache.load_to_cache(key='menu-list',
                                       value=pickle.dumps([dict(menu) for menu in menus]))

        return menus

    async def create(self, data: CreateMenu) -> Menu | None:
        row = await self.repository.create(data=data)
        if row:
            await self.cache.menu_cache_invalidation()
            return Menu(id=str(row.id),
                        title=row.title,
                        description=row.description)
        return None

    async def update(self, menu_id: UUID, data: CreateMenu) -> Menu:
        rows = await self.repository.update(menu_id=menu_id, data=data)
        if rows:
            await self.cache.menu_cache_invalidation(menu_id=str(menu_id))
            row = rows[0]
            return Menu.fill(data=row)
        raise HTTPException(status_code=404, detail='menu not found')

    async def delete(self, menu_id: UUID) -> dict | None:
        data = await self.repository.delete(menu_id=menu_id)
        if data:
            await self.cache.menu_cache_invalidation(menu_id=str(menu_id))
            return {'status': True,
                    'message': 'The menu has been deleted'}
        return None
