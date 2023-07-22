from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.schemas import Test, Menu

router = APIRouter(prefix="/menus", tags=["menu"])

test_menu = {
        "id": "a2eb416c-2245-4526-bb4b-6343d5c5016a",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }

@router.get("", response_model=List[Menu])
async def get_all_menu():
    return [Menu(**test_menu)]


@router.get("/{menu_id}", response_model=Menu)
async def get_single_menu(menu_id: UUID):
    return Menu(**test_menu)


@router.post("", response_model=Menu, status_code=201)
async def create_menu(data: Test):
    return Menu(**test_menu)


@router.put("/{menu_id}", response_model=Menu)
async def update_menu(menu_id: UUID):
    pass


@router.delete("/{menu_id}")
async def delete_menu(menu_id: UUID):
    pass
