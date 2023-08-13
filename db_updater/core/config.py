import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(__file__))
    web_app_url: str = 'http://web-app:8000/api/v1'
    menu_url: str = web_app_url + '/menus/{menu_id}'
    sub_menu_url: str = menu_url + '/submenus/{submenu_id}'
    dish_url: str = sub_menu_url + '/dishes/{dish_id}'
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbit_host: str = 'rabbitmq'
    rabbit_port: int = 5672
    path_to_menu_file: str = '/admin/Menu.xlsx'

    @property
    def rabbit_url(self):
        return f'amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}@{self.rabbit_host}:{self.rabbit_port}'
