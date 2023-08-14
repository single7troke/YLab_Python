import pytest
from core.config import Config
from core.models import Dish, Menu, SubMenu
from core.utils import delete_request, get_request, post_request
from data.data import (
    dish_create,
    dish_second_create,
    dish_third_create,
    menu_create,
    menu_second_create,
    submenu_create,
    submenu_second_create,
)

config = Config()


@pytest.fixture()
@pytest.mark.asyncio
async def create_menu():
    resp = await post_request(url=config.menu_url, menu_id='', data=menu_create)
    return Menu(**resp.data)


@pytest.fixture()
@pytest.mark.asyncio
async def create_menu_and_submenu(create_menu):
    menu = await create_menu
    resp = await post_request(url=config.sub_menu_url, menu_id=menu.id, data=submenu_create)
    return menu, SubMenu(**resp.data)


@pytest.fixture()
@pytest.mark.asyncio
async def clear_db():
    resp = await get_request(url=config.menu_url, menu_id='')
    for menu in resp.data:
        await delete_request(url=config.menu_url, menu_id=menu['id'])


@pytest.fixture()
@pytest.mark.asyncio
async def fill_db():
    resp = await post_request(url=config.menu_url, data=menu_create)
    first_menu = Menu(**resp.data)
    resp = await post_request(url=config.menu_url, data=menu_second_create)
    second_menu = Menu(**resp.data)

    resp = await post_request(url=config.sub_menu_url, menu_id=first_menu.id, data=submenu_create)
    first_sub = SubMenu(**resp.data)
    resp = await post_request(url=config.sub_menu_url, menu_id=second_menu.id, data=submenu_second_create)
    second_sub = SubMenu(**resp.data)

    resp = await post_request(url=config.dish_url, menu_id=first_menu.id, submenu_id=first_sub.id, data=dish_create)
    first_dish = Dish(**resp.data)
    resp = await post_request(url=config.dish_url, menu_id=first_menu.id, submenu_id=first_sub.id, data=dish_second_create)
    second_dish = Dish(**resp.data)
    resp = await post_request(url=config.dish_url, menu_id=second_menu.id, submenu_id=second_sub.id, data=dish_third_create)
    third_dish = Dish(**resp.data)

    return {
        'first_menu': first_menu,
        'second_menu': second_menu,
        'first_sub': first_sub,
        'second_sub': second_sub,
        'first_dish': first_dish,
        'second_dish': second_dish,
        'third_dish': third_dish
    }
