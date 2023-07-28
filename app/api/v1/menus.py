from typing import List
from uuid import UUID

from sqlalchemy import select, func, column
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, requests

from schemas import schemas
from db import models

from db.pg_db import get_session, PostgresDB

router = APIRouter(prefix="/menus", tags=["menu"])

test_menu = {
    "id": "a2eb416c-2245-4526-bb4b-6343d5c5016a",
    "title": "My menu 1",
    "description": "My menu description 1",
    "submenus_count": 0,
    "dishes_count": 0
}


@router.get("test/{test_id}")   # todo это тестовая ручка для сложного ORM запроса(не работает при пустом подменю)
async def test(test_id, session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    rows = await session.execute(
        select(column("menu_id"), func.sum(column("count")), func.count(column("sub_id"))).select_from(
            select(
            models.SubMenu.title,
                models.SubMenu.menu_id, models.SubMenu.id.label("sub_id"), func.count(models.Dish.submenu_id).label("count")).
                outerjoin(models.SubMenu).
                outerjoin(models.Menu).
                where(models.Menu.id == test_id).
                # filter(models.Menu.id == test_id).
            group_by(models.SubMenu.id)).group_by("menu_id")
    )

    res = []
    for row in rows.all():
        print(row, "======")
        res.append(row)
    print(res)
    return {"1": str(res)}


@router.get("", response_model=List[schemas.Menu])
async def get_all_menu(session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    rows = await db.get_all(models.Menu)

    return [schemas.Menu(id=str(i.id),
                         title=i.title,
                         description=i.description,
                         submenus_count=i.submenu_counter,
                         dishes_count=i.dish_counter) for i in rows]


@router.get("/{menu_id}")
async def get_single_menu(menu_id: UUID,
                          session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.get_one(_id=str(menu_id), model=models.Menu)
    if row:
        return schemas.Menu(id=str(row.id),
                            title=row.title,
                            description=row.description,
                            submenus_count=row.submenu_counter,
                            dishes_count=row.dish_counter)
    raise HTTPException(status_code=404,
                        detail="menu not found")


@router.post("", response_model=schemas.Menu, status_code=201)
async def create_menu(body: schemas.CreateMenu,
                      session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.create(models.Menu, **dict(body))
    return schemas.Menu(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        submenus_count=row.submenu_counter,
                        dishes_count=row.dish_counter)


@router.patch("/{menu_id}", status_code=200)
async def update_menu(menu_id: UUID,
                      data: schemas.CreateMenu,
                      session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.update(menu_id, model=models.Menu, data=data)
    return schemas.Menu(id=str(row.id),
                        title=row.title,
                        description=row.description,
                        submenus_count=row.submenu_counter,
                        dishes_count=row.dish_counter)


@router.delete("/{menu_id}")
async def delete_menu(menu_id: UUID,
                      session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    await db.delete(menu_id, model=models.Menu)
    return {"status": True,
            "message": "The menu has been deleted"}
