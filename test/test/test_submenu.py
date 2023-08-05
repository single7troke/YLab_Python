import pytest

from core.config import Config
from core.models import Menu, SubMenu
from core.utils import get_request, post_request, update_request, delete_request, check_header
from data.data import submenu_create, submenu_update, submenu_delete

config = Config()

MENU: Menu | None = None
SUBMENU: SubMenu | None = None


@pytest.mark.order(2)
@pytest.mark.asyncio
class TestSubmenu:
    async def test_no_any_submenu_in_menu(self, create_menu, clear_db):
        await clear_db
        global MENU
        MENU = await create_menu
        resp = await get_request(url=config.sub_menu_url, menu_id=MENU.id, submenu_id="")
        assert resp.status_code == 200
        assert resp.data == []

    async def test_create_submenu(self):
        resp = await post_request(url=config.sub_menu_url, menu_id=MENU.id, data=submenu_create)
        assert resp.status_code == 201
        assert check_header(resp.headers)
        assert resp.data["title"] == submenu_create["title"]
        assert resp.data["description"] == submenu_create["description"]
        global SUBMENU
        SUBMENU = SubMenu(**resp.data)

    async def test_get_single_submenu(self):
        resp = await get_request(url=config.sub_menu_url, menu_id=MENU.id, submenu_id=SUBMENU.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == dict(SUBMENU)

    async def test_get_all_submenu(self):
        resp = await get_request(url=config.sub_menu_url, menu_id=MENU.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == [dict(SUBMENU)]

    async def test_update_submenu(self):
        global SUBMENU
        resp = await update_request(url=config.sub_menu_url, menu_id=MENU.id, submenu_id=SUBMENU.id,
                                    data=submenu_update)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data["id"] == SUBMENU.id
        assert resp.data["title"] == submenu_update["title"]
        assert resp.data["description"] == submenu_update["description"]
        assert resp.data["dishes_count"] == SUBMENU.dishes_count
        SUBMENU = SubMenu(**resp.data)

    async def test_delete_submenu(self):
        resp = await delete_request(url=config.sub_menu_url, menu_id=MENU.id, submenu_id=SUBMENU.id)
        assert resp.status_code == 200
        assert check_header(resp.headers)
        assert resp.data == submenu_delete

    async def test_submenu_have_been_deleted(self, clear_db):
        resp = await get_request(url=config.sub_menu_url, menu_id=MENU.id, submenu_id=SUBMENU.id)
        assert resp.status_code == 404
        assert check_header(resp.headers)
        assert resp.data == {"detail": "submenu not found"}
        await clear_db
