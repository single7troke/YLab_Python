from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.schemas import Dish

router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["dish"])


@router.get("", response_model=list[Dish])
async def get_all_dishes(menu_id: UUID, submenu_id: UUID):
    pass


@router.get("/{dish_id}", response_model=Dish)
async def get_single_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    pass


@router.post("", response_model=Dish)
async def create_dish(menu_id: UUID, submenu_id: UUID):
    return {"hello": menu_id}


@router.put("/{dish_id}", response_model=Dish)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    pass


@router.delete("/{dish_id}")
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    pass
