import pytest

from core.config import Config
from core.models import Menu
from core.utils import get_request, post_request, delete_request, update_request, check_header
from data.data import menu_create, menu_deleted, menu_update

config = Config()

MENU: Menu | None = None


@pytest.mark.order(1)
@pytest.mark.asyncio
class TestMenu:
    async def test_no_any_menu_in_db(self, clear_db):
        await clear_db
        resp = await get_request(url=config.menu_url)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == []

    async def test_create(self):
        resp = await post_request(url=config.menu_url, data=menu_create)
        assert resp.status_code == 201
        assert check_header(resp.headers)
        assert resp.data["title"] == menu_create["title"]
        assert resp.data["description"] == menu_create["description"]
        assert resp.data["submenus_count"] == 0
        assert resp.data["dishes_count"] == 0
        global MENU
        MENU = Menu(**resp.data)

    async def test_get_all_menu(self):
        resp = await get_request(url=config.menu_url)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == [dict(MENU)]

    async def test_get_single_menu(self):
        resp = await get_request(config.menu_url, menu_id=MENU.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == dict(MENU)

    async def test_update_menu(self, clear_db):
        global MENU
        resp = await update_request(config.menu_url, menu_id=MENU.id, data=menu_update)
        assert resp.status_code == 200
        assert resp.data["id"] == MENU.id
        assert resp.data["title"] == menu_update["title"]
        assert resp.data["description"] == menu_update["description"]
        assert resp.data["submenus_count"] == MENU.submenus_count
        assert resp.data["dishes_count"] == MENU.dishes_count
        await clear_db

    async def test_delete(self):
        resp = await delete_request(url=config.menu_url, menu_id=MENU.id)
        assert resp.status_code == 200
        assert resp.data == menu_deleted

    async def test_menu_have_been_deleted(self):
        resp = await get_request(url=config.menu_url, menu_id=MENU.id)
        assert resp.status_code == 404
        assert resp.data == {'detail': 'menu not found'}
