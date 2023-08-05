from uuid import UUID

from fastapi import Depends, HTTPException

from db.filters import GetSingleSubmenuFilter, GetAllSubmenusFilter
from db.repositories import SubmenuRepository
from schemas.schemas import SubMenu, CreateMenu


class SubmenuService:
    def __init__(self, repository: SubmenuRepository = Depends(SubmenuRepository)):
        self.repository = repository

    async def get(self, submenu_id: UUID) -> SubMenu:
        rows = await self.repository.get(custom_filter=GetSingleSubmenuFilter(_id=submenu_id))
        if rows:
            row = rows[0]
            return SubMenu(id=str(row.id),
                           title=row.title,
                           description=row.description,
                           dishes_count=row.dishes_count)
        raise HTTPException(status_code=404, detail="submenu not found")

    async def list(self, menu_id: UUID) -> list[SubMenu]:
        rows = await self.repository.get(custom_filter=GetAllSubmenusFilter(_id=menu_id))
        return [SubMenu(id=str(i.id),
                        title=i.title,
                        description=i.description,
                        dishes_count=i.dishes_count) for i in rows]

    async def create(self, menu_id: UUID, data: CreateMenu) -> SubMenu:
        row = await self.repository.create(menu_id=menu_id, data=data)
        if row:
            return SubMenu(id=str(row.id),
                           title=row.title,
                           description=row.description,
                           dishes_count=0)

    async def update(self, submenu_id: UUID, data: CreateMenu) -> SubMenu:
        rows = await self.repository.update(submenu_id=submenu_id, data=data)
        if rows:
            row = rows[0]
            return SubMenu(id=str(row.id),
                           title=row.title,
                           description=row.description,
                           dishes_count=row.dishes_count)
        raise HTTPException(status_code=404, detail="submenu not found")

    async def delete(self, submenu_id: UUID) -> dict:
        data = await self.repository.delete(submenu_id=submenu_id)
        if data:
            return {"status": True,
                    "message": "The submenu has been deleted"}
