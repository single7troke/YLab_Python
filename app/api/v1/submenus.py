from uuid import UUID

from fastapi import APIRouter, Depends
from schemas import CreateSubmenu, SubMenu
from services.submenu_service import SubmenuService

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenu'])


@router.get('', response_model=SubMenu, status_code=200)
async def get_all_submenu(menu_id: UUID,
                          submenu: SubmenuService = Depends(SubmenuService)):
    submenus = await submenu.list(menu_id=menu_id)
    return submenus


@router.get('/{submenu_id}')
async def get_single_submenu(menu_id: UUID,
                             submenu_id: UUID,
                             submenu: SubmenuService = Depends(SubmenuService)):
    submenu = await submenu.get(submenu_id=submenu_id)
    return submenu


@router.post('', response_model=SubMenu, status_code=201)
async def create_submenu(body: CreateSubmenu,
                         menu_id: UUID,
                         submenu: SubmenuService = Depends(SubmenuService)):
    new_submenu = await submenu.create(menu_id=menu_id, data=body)
    return new_submenu


@router.patch('/{submenu_id}', response_model=SubMenu, status_code=200)
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         body: CreateSubmenu,
                         submenu: SubmenuService = Depends(SubmenuService)):
    updated_menu = await submenu.update(menu_id=menu_id, submenu_id=submenu_id, data=body)
    return updated_menu


@router.delete('/{submenu_id}')
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         submenu: SubmenuService = Depends(SubmenuService)):
    data = await submenu.delete(menu_id=menu_id, submenu_id=submenu_id)
    return data
