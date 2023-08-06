import pytest
from core.config import Config
from core.utils import delete_request, get_request, post_request
from data.data import (
    dish_create,
    dish_second_create,
    menu_create,
    submenu_create,
    submenu_second_create,
)

config = Config()

MENU_ID: str | None = None
FIRST_SUBMENU_ID: str | None = None
SECOND_SUBMENU_ID: str | None = None
FIRST_DISH_ID: str | None = None
SECOND_DISH_ID: str | None = None


@pytest.mark.order(4)
@pytest.mark.asyncio
class TestCountDishesAndSubmenu:
    async def test_create_menu(self, clear_db):
        await clear_db
        resp = await post_request(url=config.menu_url, data=menu_create)
        assert resp.status_code == 201
        assert resp.data['submenus_count'] == 0
        assert resp.data['dishes_count'] == 0
        global MENU_ID
        MENU_ID = resp.data['id']

    async def test_create_first_submenu(self):
        global FIRST_SUBMENU_ID
        resp = await post_request(url=config.sub_menu_url,
                                  menu_id=MENU_ID,
                                  data=submenu_create)
        assert resp.status_code == 201
        assert resp.data['dishes_count'] == 0
        FIRST_SUBMENU_ID = resp.data['id']
        resp = await get_request(url=config.menu_url,
                                 menu_id=MENU_ID)
        assert resp.status_code == 200
        assert resp.data['submenus_count'] == 1
        assert resp.data['dishes_count'] == 0

    async def test_create_first_dish(self):
        global FIRST_DISH_ID
        dish = await post_request(url=config.dish_url,
                                  menu_id=MENU_ID,
                                  submenu_id=FIRST_SUBMENU_ID,
                                  data=dish_create)
        assert dish.status_code == 201
        FIRST_DISH_ID = dish.data['id']
        menu = await get_request(url=config.menu_url,
                                 menu_id=MENU_ID)
        assert menu.status_code == 200
        assert menu.data['submenus_count'] == 1
        assert menu.data['dishes_count'] == 1
        submenu = await get_request(url=config.sub_menu_url,
                                    menu_id=MENU_ID,
                                    submenu_id=FIRST_SUBMENU_ID)
        assert submenu.status_code == 200
        assert submenu.data['dishes_count'] == 1

    async def test_create_second_dish(self):
        global SECOND_DISH_ID
        dish = await post_request(url=config.dish_url,
                                  menu_id=MENU_ID,
                                  submenu_id=FIRST_SUBMENU_ID,
                                  data=dish_second_create)
        assert dish.status_code == 201
        SECOND_DISH_ID = dish.data['id']
        menu = await get_request(url=config.menu_url,
                                 menu_id=MENU_ID)
        assert menu.status_code == 200
        assert menu.data['submenus_count'] == 1
        assert menu.data['dishes_count'] == 2
        submenu = await get_request(url=config.sub_menu_url,
                                    menu_id=MENU_ID,
                                    submenu_id=FIRST_SUBMENU_ID)
        assert submenu.status_code == 200
        assert submenu.data['dishes_count'] == 2

    async def test_create_second_submenu(self):
        global SECOND_SUBMENU_ID
        submenu = await post_request(url=config.sub_menu_url,
                                     menu_id=MENU_ID,
                                     data=submenu_second_create)
        assert submenu.status_code == 201
        assert submenu.data['dishes_count'] == 0
        SECOND_SUBMENU_ID = submenu.data['id']
        menu = await get_request(url=config.menu_url,
                                 menu_id=MENU_ID)
        assert menu.status_code == 200
        assert menu.data['submenus_count'] == 2
        assert menu.data['dishes_count'] == 2

    async def test_delete_first_submenu(self):
        resp = await delete_request(url=config.sub_menu_url,
                                    menu_id=MENU_ID,
                                    submenu_id=FIRST_SUBMENU_ID)
        assert resp.status_code == 200
        menu = await get_request(url=config.menu_url,
                                 menu_id=MENU_ID)
        assert menu.data['submenus_count'] == 1
        assert menu.data['dishes_count'] == 0

    async def test_delete_second_submenu(self):
        resp = await delete_request(url=config.sub_menu_url,
                                    menu_id=MENU_ID,
                                    submenu_id=SECOND_SUBMENU_ID)
        assert resp.status_code == 200
        menu = await get_request(url=config.menu_url,
                                 menu_id=MENU_ID)
        assert menu.data['submenus_count'] == 0
        assert menu.data['dishes_count'] == 0

    async def test_no_dishes_in_db(self):
        first_submenu_dish_list = await get_request(url=config.dish_url,
                                                    menu_id=MENU_ID,
                                                    submenu_id=FIRST_SUBMENU_ID)
        second_submenu_dish_list = await get_request(url=config.dish_url,
                                                     menu_id=MENU_ID,
                                                     submenu_id=SECOND_SUBMENU_ID)
        assert first_submenu_dish_list.status_code == 200
        assert first_submenu_dish_list.data == []
        assert second_submenu_dish_list.status_code == 200
        assert second_submenu_dish_list.data == []

    async def test_no_submenus_in_db(self):
        submenu_list = await get_request(url=config.sub_menu_url,
                                         menu_id=MENU_ID)
        assert submenu_list.status_code == 200
        assert submenu_list.data == []

    async def test_delete_menu(self):
        resp = await delete_request(url=config.menu_url,
                                    menu_id=MENU_ID)
        assert resp.status_code == 200

    async def test_no_menu_in_db(self):
        menu_list = await get_request(config.menu_url)
        assert menu_list.status_code == 200
        assert menu_list.data == []
