from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.schemas import SubMenu

router = APIRouter(prefix="/menus/{menu_id}/submenus", tags=["submenu"])


@router.get("", response_model=list[SubMenu])
async def get_all_submenu(menu_id: UUID):
    pass


@router.get("/{submenu_id}", response_model=SubMenu)
async def get_single_submenu(menu_id: UUID, submenu_id: UUID):
    pass


@router.post("", response_model=SubMenu)
async def create_submenu(menu_id: UUID):
    return {"hello": menu_id}


@router.put("/{submenu_id}", response_model=SubMenu)
async def update_submenu(menu_id: UUID, submenu_id: UUID):
    pass


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: UUID, submenu_id: UUID):
    pass
