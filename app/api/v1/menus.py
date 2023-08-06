from uuid import UUID

from fastapi import APIRouter, Depends
from schemas import CreateMenu, Menu
from services import MenuService

router = APIRouter(prefix='/menus', tags=['menu'])


@router.get('', response_model=list[Menu])
async def get_all_menu(menu: MenuService = Depends(MenuService)):

    rows = await menu.list()
    return rows


@router.get('/{menu_id}', response_model=Menu)
async def get_single_menu(menu_id: UUID,
                          menu: MenuService = Depends(MenuService)):
    data = await menu.get(menu_id=menu_id)
    return data


@router.post('', response_model=Menu, status_code=201)
async def create_menu(body: CreateMenu,
                      menu: MenuService = Depends(MenuService)):
    new_menu = await menu.create(data=body)
    return new_menu


@router.patch('/{menu_id}', response_model=Menu, status_code=200)
async def update_menu(menu_id: UUID,
                      data: CreateMenu,
                      menu: MenuService = Depends(MenuService)):
    updated_menu = await menu.update(menu_id=menu_id, data=data)
    return updated_menu


@router.delete('/{menu_id}')
async def delete_menu(menu_id: UUID,
                      menu: MenuService = Depends(MenuService)):
    data = await menu.delete(menu_id=menu_id)
    return data
