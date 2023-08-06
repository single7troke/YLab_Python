from fastapi import APIRouter

from api.v1.menus import router as menu_router
from api.v1.submenus import router as submenu_router
from api.v1.dishes import router as dish_router

router = APIRouter(prefix='/v1')

router.include_router(menu_router)
router.include_router(submenu_router)
router.include_router(dish_router)
