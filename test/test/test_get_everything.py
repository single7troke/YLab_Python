import pytest
from core.config import Config
from core.utils import delete_request, get_request
from data.data import construct_expected_resp_from_everything

config = Config()

DATA: dict | None = None
EXPECTED: list | None = None


@pytest.mark.order(5)
@pytest.mark.asyncio
class TestEndpointEverything:
    async def test_db_is_empty(self, clear_db):
        await clear_db
        resp = await get_request(url=config.everything_url)
        assert resp.status_code == 200
        assert resp.data == []

    async def test_everything(self, fill_db):
        global DATA
        global EXPECTED
        DATA = await fill_db
        EXPECTED = construct_expected_resp_from_everything(DATA)

        resp = await get_request(url=config.everything_url)
        assert resp.status_code == 200
        assert EXPECTED == resp.data

        await delete_request(url=config.menu_url, menu_id=DATA['second_menu'].id)
        EXPECTED.pop(1)
        resp = await get_request(url=config.everything_url)
        assert resp.status_code == 200
        assert EXPECTED == resp.data

        await delete_request(url=config.menu_url, menu_id=DATA['first_menu'].id)
        EXPECTED.pop(0)
        resp = await get_request(url=config.everything_url)
        assert resp.status_code == 200
        assert EXPECTED == resp.data
