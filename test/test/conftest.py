import pytest

from core.config import Config
from core.models import Menu, SubMenu
from data.data import menu_create, submenu_create
from core.utils import get_request, post_request, delete_request


config = Config()


@pytest.fixture()
async def create_menu():
    resp = await post_request(url=config.menu_url, menu_id="", data=menu_create)
    return Menu(**resp.data)


@pytest.fixture()
async def create_menu_and_submenu(create_menu):
    menu = await create_menu
    resp = await post_request(url=config.sub_menu_url, menu_id=menu.id, data=submenu_create)
    return menu, SubMenu(**resp.data)


@pytest.fixture()
async def clear_db():
    resp = await get_request(url=config.menu_url, menu_id="")
    for menu in resp.data:
        await delete_request(url=config.menu_url, menu_id=menu["id"])
