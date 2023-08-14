import pickle
from uuid import UUID

from db.filters import GetAllSubmenusFilter, GetSingleSubmenuFilter
from db.repositories import SubmenuRepository
from fastapi import BackgroundTasks, Depends, HTTPException
from schemas import CreateSubmenu, SubMenu
from services import CacheService


class SubmenuService:
    def __init__(self,
                 repository: SubmenuRepository = Depends(SubmenuRepository),
                 cache: CacheService = Depends(CacheService)):
        self.repository = repository
        self.cache = cache

    async def get(self, submenu_id: UUID) -> SubMenu:
        data_from_cache = await self.cache.get_from_cache(key=str(submenu_id))
        if data_from_cache:
            return SubMenu(**pickle.loads(data_from_cache))
        rows = await self.repository.get(custom_filter=GetSingleSubmenuFilter(_id=submenu_id))
        if rows:
            submenu = SubMenu.fill(rows[0])
            await self.cache.load_to_cache(key=str(submenu_id), value=pickle.dumps(dict(submenu)))
            return submenu
        raise HTTPException(status_code=404, detail='submenu not found')

    async def list(self, menu_id: UUID) -> list[SubMenu]:
        data_from_cache = await self.cache.get_from_cache(key=f'{menu_id}-submenu-list')
        if data_from_cache:
            submenus = [SubMenu(**submenu) for submenu in pickle.loads(data_from_cache)]
            return submenus
        rows = await self.repository.get(custom_filter=GetAllSubmenusFilter(_id=menu_id))
        submenus = [SubMenu.fill(data=row) for row in rows]
        await self.cache.load_to_cache(
            key=f'{menu_id}-submenu-list',
            value=pickle.dumps([dict(submenu) for submenu in submenus]))
        return submenus

    async def create(self,
                     menu_id: UUID,
                     task: BackgroundTasks,
                     data: CreateSubmenu) -> SubMenu | None:
        row = await self.repository.create(menu_id=menu_id, data=data)
        if row:
            task.add_task(self.cache.submenu_cache_invalidation, menu_id=str(menu_id))
            # await self.cache.submenu_cache_invalidation(menu_id=str(menu_id))
            return SubMenu(id=str(row.id),
                           title=row.title,
                           description=row.description,
                           dishes_count=0)
        return None

    async def update(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     task: BackgroundTasks,
                     data: CreateSubmenu) -> SubMenu:
        rows = await self.repository.update(submenu_id=submenu_id, data=data)
        if rows:
            task.add_task(self.cache.submenu_cache_invalidation,
                          menu_id=str(menu_id),
                          submenu_id=str(submenu_id))
            # await self.cache.submenu_cache_invalidation(menu_id=str(menu_id), submenu_id=str(submenu_id))
            return SubMenu.fill(rows[0])
        raise HTTPException(status_code=404, detail='submenu not found')

    async def delete(self,
                     menu_id: UUID,
                     task: BackgroundTasks,
                     submenu_id: UUID) -> dict | None:
        data = await self.repository.delete(submenu_id=submenu_id)
        if data:
            task.add_task(self.cache.submenu_cache_invalidation,
                          menu_id=str(menu_id),
                          submenu_id=str(submenu_id))
            # await self.cache.submenu_cache_invalidation(menu_id=str(menu_id), submenu_id=str(submenu_id))
            return {'status': True,
                    'message': 'The submenu has been deleted'}
        return None
