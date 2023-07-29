import aiohttp
import json
from core.config import Config
from core.models import Response

config = Config()


def construct_url(url: str, menu_id="", submenu_id="", dish_id=""):
    return url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


def check_header(headers):
    return headers["Content-Type"] == "application/json"


async def get_request(url, menu_id="", submenu_id="", dish_id="") -> Response:
    url = construct_url(url, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return Response(data=data, status_code=resp.status, headers=resp.headers)


async def post_request(url, data, menu_id="", submenu_id="", dish_id="") -> Response:
    url = construct_url(url, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url,
                                data=json.dumps(data),
                                headers={'content-type': 'application/json'}) as resp:
            data = await resp.json()
            return Response(data=data, status_code=resp.status, headers=resp.headers)


async def update_request(url, data, menu_id="", submenu_id="", dish_id="") -> Response:
    url = construct_url(url=url, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=url,
                                 data=json.dumps(data),
                                 headers={'content-type': 'application/json'}) as resp:
            data = await resp.json()
            return Response(data=data, status_code=resp.status, headers=resp.headers)


async def delete_request(url, menu_id="", submenu_id="", dish_id="") -> Response:
    url = construct_url(url=url, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    async with aiohttp.ClientSession() as session:
        async with session.delete(url=url) as resp:
            data = await resp.json()
            return Response(data=data, status_code=resp.status, headers=resp.headers)
