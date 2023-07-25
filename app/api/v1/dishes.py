from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas import Dish, CreateDish
from db import models
from db.pg_db import PostgresDB, get_session
from db import models

router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["dish"])


@router.get("", response_model=list[Dish])
async def get_all_dishes(menu_id: UUID,
                         submenu_id: UUID,
                         session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    rows = await db.get_all(model=models.Dish)
    return [Dish(id=str(row.id),
                 title=row.title,
                 description=row.description,
                 price=row.price) for row in rows]


@router.get("/{dish_id}")
async def get_single_dish(menu_id: UUID,
                          submenu_id: UUID,
                          dish_id: UUID,
                          session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.get_one(_id=str(dish_id), model=models.Dish)
    if row:
        return Dish(id=str(row.id),
                    title=row.title,
                    description=row.description,
                    price=row.price)
    raise HTTPException(status_code=404,
                        detail="dish not found")


@router.post("", response_model=Dish, status_code=201)
async def create_dish(menu_id: UUID,
                      submenu_id: UUID,
                      body: CreateDish,
                      session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.create(model=models.Dish, menu_id=menu_id, submenu_id=submenu_id, **dict(body))
    return Dish(id=str(row.id),
                title=row.title,
                description=row.description,
                price=row.price)


@router.patch("/{dish_id}", response_model=Dish)
async def update_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      body: CreateDish,
                      session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    row = await db.update(_id=dish_id, model=models.Dish, data=body)
    return Dish(id=str(row.id),
                title=row.title,
                description=row.description,
                price=row.price)


@router.delete("/{dish_id}")
async def delete_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      session: AsyncSession = Depends(get_session)):
    db = PostgresDB(session)
    await db.delete(_id=str(dish_id), model=models.Dish)
    return {"status": True,
            "message": "The dish has been deleted"}