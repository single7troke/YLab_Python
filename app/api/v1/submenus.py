from uuid import UUID

from fastapi import APIRouter, Depends

from schemas import schemas
from services.submenu_service import SubmenuService

router = APIRouter(prefix="/menus/{menu_id}/submenus", tags=["submenu"])


@router.get("")
async def get_all_submenu(menu_id: UUID,
                          submenu: SubmenuService = Depends(SubmenuService)):
    submenus = await submenu.list(menu_id=menu_id)
    return submenus


@router.get("/{submenu_id}")
async def get_single_submenu(menu_id: UUID,
                             submenu_id: UUID,
                             submenu: SubmenuService = Depends(SubmenuService)):
    submenu = await submenu.get(submenu_id=submenu_id)
    return submenu


@router.post("", status_code=201)
async def create_submenu(body: schemas.CreateMenu,
                         menu_id: UUID,
                         submenu: SubmenuService = Depends(SubmenuService)):
    new_submenu = await submenu.create(menu_id=menu_id, data=body)
    return new_submenu


@router.patch("/{submenu_id}")
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         body: schemas.CreateMenu,
                         submenu: SubmenuService = Depends(SubmenuService)):
    updated_menu = await submenu.update(submenu_id=submenu_id, data=body)
    return updated_menu


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         submenu: SubmenuService = Depends(SubmenuService)):
    data = await submenu.delete(submenu_id=submenu_id)
    return data
