import hashlib
import json

import requests
from core.config import Config
from core.models import Response

config = Config()


def get_hash(path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def construct_url(url_type: str, menu_id='', submenu_id='', dish_id=''):
    if url_type == 'menu':
        return config.menu_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    elif url_type == 'submenu':
        return config.sub_menu_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    else:
        return config.dish_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


def get_request(url_type, menu_id='', submenu_id='', dish_id='') -> Response:
    url = construct_url(url_type=url_type, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    response = requests.get(url=url)
    return response.json()


def post_request(url_type, data, menu_id='', submenu_id='', dish_id='') -> Response:
    url = construct_url(url_type=url_type, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    response = requests.post(url=url,
                             data=json.dumps(data),
                             headers={'content-type': 'application/json'})
    return response.json()


def update_request(url_type, data, menu_id='', submenu_id='', dish_id='') -> Response:
    url = construct_url(url_type=url_type, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    response = requests.patch(url=url,
                              data=json.dumps(data),
                              headers={'content-type': 'application/json'})
    return response.json()


def delete_request(url_type, menu_id='', submenu_id='', dish_id='') -> Response:
    url = construct_url(url_type=url_type, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    response = requests.delete(url=url)
    return response.json()
