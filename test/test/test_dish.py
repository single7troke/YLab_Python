import pytest
from core.config import Config
from core.models import Dish, Menu, SubMenu
from core.utils import (
    check_header,
    delete_request,
    get_request,
    post_request,
    update_request,
)
from data.data import dish_create, dish_delete, dish_update

config = Config()

MENU: Menu | None = None
SUBMENU: SubMenu | None = None
DISH: Dish | None = None


@pytest.mark.order(3)
@pytest.mark.asyncio
class TestDish:
    async def test_no_any_dish_in_submenu(self, create_menu_and_submenu, clear_db):
        await clear_db
        global MENU, SUBMENU
        MENU, SUBMENU = await create_menu_and_submenu
        resp = await get_request(config.dish_url,
                                 menu_id=MENU.id,
                                 submenu_id=SUBMENU.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == []

    async def test_create_dish(self):
        resp = await post_request(config.dish_url,
                                  menu_id=MENU.id,
                                  submenu_id=SUBMENU.id,
                                  data=dish_create)
        assert resp.status_code == 201
        assert check_header(resp.headers)
        assert resp.data['title'] == dish_create['title']
        assert resp.data['description'] == dish_create['description']
        assert resp.data['price'] == dish_create['price']
        global DISH
        DISH = Dish(**resp.data)

    async def test_get_single_dish(self):
        resp = await get_request(url=config.dish_url,
                                 menu_id=MENU.id,
                                 submenu_id=SUBMENU.id,
                                 dish_id=DISH.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == dict(DISH)

    async def test_get_all_dishes(self):
        resp = await get_request(url=config.dish_url,
                                 menu_id=MENU.id,
                                 submenu_id=SUBMENU.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == [dict(DISH)]

    async def test_update_dish(self):
        global DISH
        resp = await update_request(url=config.dish_url,
                                    menu_id=MENU.id,
                                    submenu_id=SUBMENU.id,
                                    dish_id=DISH.id,
                                    data=dish_update)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data['id'] == DISH.id
        assert resp.data['title'] == dish_update['title']
        assert resp.data['description'] == dish_update['description']
        assert resp.data['price'] == dish_update['price']
        DISH = Dish(**resp.data)

    async def test_delete_dish(self):
        resp = await delete_request(url=config.dish_url,
                                    menu_id=MENU.id,
                                    submenu_id=SUBMENU.id,
                                    dish_id=DISH.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == dish_delete

    async def test_get_dish_that_not_in_db(self):
        resp = await get_request(url=config.dish_url,
                                 menu_id=MENU.id,
                                 submenu_id=SUBMENU.id,
                                 dish_id=DISH.id)
        assert resp.status_code == 404
        assert check_header(resp.headers)
        assert resp.data == {'detail': 'dish not found'}
