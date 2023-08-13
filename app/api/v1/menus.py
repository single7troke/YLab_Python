from uuid import UUID

from fastapi import APIRouter, Depends
from schemas import CreateMenu, Everything, Menu
from services import MenuService

router = APIRouter(prefix='/menus', tags=['menu'])


@router.get('',
            response_model=list[Menu],
            summary='Menu list',
            description='Returns menu list with submenu count and dish count')
async def get_all_menu(menu: MenuService = Depends(MenuService)):
    rows = await menu.list()
    return rows


@router.get('/everything',
            response_model=list[Everything],
            summary='Get all from DB',
            description='Gets all data from database')
async def get_all(menu: MenuService = Depends(MenuService)):
    data = await menu.get_all_data()
    return data


@router.get('/{menu_id}',
            response_model=Menu,
            summary='Single menu',
            description='Returns menu with submenu count and dish count')
async def get_single_menu(menu_id: UUID,
                          menu: MenuService = Depends(MenuService)):
    data = await menu.get(menu_id=menu_id)
    return data


@router.post('',
             response_model=Menu,
             status_code=201,
             summary='New menu',
             description='Creates new menu and returns it')
async def create_menu(body: CreateMenu,
                      menu: MenuService = Depends(MenuService)):
    new_menu = await menu.create(data=body)
    return new_menu


@router.patch('/{menu_id}',
              response_model=Menu,
              status_code=200,
              summary='Update menu',
              description='Updates menu and returns updated menu')
async def update_menu(menu_id: UUID,
                      data: CreateMenu,
                      menu: MenuService = Depends(MenuService)):
    updated_menu = await menu.update(menu_id=menu_id, data=data)
    return updated_menu


@router.delete('/{menu_id}',
               summary='Delete menu',
               description='Deletes menu and returns message that menu have been deleted')
async def delete_menu(menu_id: UUID,
                      menu: MenuService = Depends(MenuService)):
    data = await menu.delete(menu_id=menu_id)
    return data
