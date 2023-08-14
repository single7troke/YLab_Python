from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from schemas import CreateSubmenu, SubMenu
from services.submenu_service import SubmenuService

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenu'])


@router.get('',
            response_model=list[SubMenu],
            status_code=200,
            summary='Submenu list',
            description='Returns submenu list with dish count')
async def get_all_submenu(menu_id: UUID,
                          submenu: SubmenuService = Depends(SubmenuService)):
    submenus = await submenu.list(menu_id=menu_id)
    return submenus


@router.get('/{submenu_id}',
            status_code=200,
            summary='Single submenu',
            description='Returns submenu with dish count'
            )
async def get_single_submenu(menu_id: UUID,
                             submenu_id: UUID,
                             submenu: SubmenuService = Depends(SubmenuService)):
    submenu = await submenu.get(submenu_id=submenu_id)
    return submenu


@router.post('',
             response_model=SubMenu,
             status_code=201,
             summary='New submenu',
             description='Creates new submenu and returns it')
async def create_submenu(body: CreateSubmenu,
                         menu_id: UUID,
                         task: BackgroundTasks,
                         submenu: SubmenuService = Depends(SubmenuService)):
    new_submenu = await submenu.create(menu_id=menu_id, data=body, task=task)
    return new_submenu


@router.patch('/{submenu_id}',
              response_model=SubMenu,
              status_code=200,
              summary='Update submenu',
              description='Updates submenu and returns updated submenu')
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         body: CreateSubmenu,
                         task: BackgroundTasks,
                         submenu: SubmenuService = Depends(SubmenuService)):
    updated_menu = await submenu.update(menu_id=menu_id, submenu_id=submenu_id, data=body, task=task)
    return updated_menu


@router.delete('/{submenu_id}',
               summary='Delete submenu',
               description='Deletes submenu and returns message that submenu have been deleted')
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         task: BackgroundTasks,
                         submenu: SubmenuService = Depends(SubmenuService)):
    data = await submenu.delete(menu_id=menu_id, submenu_id=submenu_id, task=task)
    return data
