import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_app_url: str = "http://web-app:8000/api/v1"
    menu_url: str = web_app_url + "/menus/{menu_id}"
    sub_menu_url: str = menu_url + "/submenus/{submenu_id}"
    dish_url: str = sub_menu_url + "/dishes/{dish_id}"
