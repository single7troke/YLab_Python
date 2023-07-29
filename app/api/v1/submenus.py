from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import schemas
from db import models
from db.pg_db import get_session, PostgresDB

router = APIRouter(prefix="/menus/{menu_id}/submenus", tags=["submenu"])


@router.get("")
async def get_all_submenu(menu_id: UUID,
                          session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    rows = await db.get_all(models.SubMenu, _id=menu_id)
    return [schemas.SubMenu(id=str(i.id),
                            title=i.title,
                            description=i.description,
                            dishes_count=i.dish_counter) for i in rows]


@router.get("/{submenu_id}")
async def get_single_submenu(menu_id: UUID,
                             submenu_id: UUID,
                             session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.get_one(_id=str(submenu_id), model=models.SubMenu)
    if row:
        return schemas.SubMenu(id=str(row.id),
                               title=row.title,
                               description=row.description,
                               dishes_count=row.dish_counter)
    raise HTTPException(status_code=404,
                        detail="submenu not found")


@router.post("", status_code=201)
async def create_submenu(body: schemas.CreateMenu,
                         menu_id: UUID,
                         session: AsyncSession = Depends(get_session)
                         ):
    db = PostgresDB(session)
    row = await db.create(models.SubMenu, menu_id=menu_id, **dict(body))
    return schemas.SubMenu(id=str(row.id),
                           title=row.title,
                           description=row.description,
                           dishes_count=row.dish_counter)


@router.patch("/{submenu_id}")
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         body: schemas.CreateMenu,
                         session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.update(_id=submenu_id, model=models.SubMenu, data=body)
    return schemas.SubMenu(id=str(row.id),
                           title=row.title,
                           description=row.description,
                           dishes_count=row.dish_counter)


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    await db.delete(_id=submenu_id, model=models.SubMenu)
    return {"status": True,
            "message": "The submenu has been deleted"}
