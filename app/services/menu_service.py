from uuid import UUID

from fastapi import Depends, HTTPException

from db.repositories import MenuRepository
from db.filters import GetAllMenusFilter, GetSingleMenuFilter
from schemas.schemas import Menu, CreateMenu


class MenuService:
    def __init__(self, repository: MenuRepository = Depends(MenuRepository)):
        self.repository = repository

    async def get(self, menu_id: UUID) -> Menu:
        rows = await self.repository.get(custom_filter=GetSingleMenuFilter(_id=menu_id))
        if rows:
            row = rows[0]
            return Menu(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        submenus_count=row.submenus_count,
                        dishes_count=row.dishes_count)
        raise HTTPException(status_code=404, detail="menu not found")

    async def list(self) -> list[Menu]:
        rows = await self.repository.get(custom_filter=GetAllMenusFilter())
        return [Menu(id=str(i.id),
                     title=i.title,
                     description=i.description,
                     submenus_count=i.submenus_count,
                     dishes_count=i.dishes_count) for i in rows]

    async def create(self, data: CreateMenu) -> Menu:
        row = await self.repository.create(data=data)
        if row:
            return Menu(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        submenus_count=0,
                        dishes_count=0)

    async def update(self, menu_id: UUID, data: CreateMenu) -> Menu:
        rows = await self.repository.update(menu_id=menu_id, data=data)
        if rows:
            row = rows[0]
            return Menu(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        submenus_count=row.submenus_count,
                        dishes_count=row.dishes_count)
        raise HTTPException(status_code=404, detail="menu not found")

    async def delete(self, menu_id: UUID) -> dict:
        data = await self.repository.delete(menu_id=menu_id)
        if data:
            return {"status": True,
                    "message": "The menu has been deleted"}
