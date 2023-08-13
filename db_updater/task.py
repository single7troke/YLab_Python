import logging

from celery import Celery
from core import parser, reader
from core.config import Config
from core.models import Types
from core.utils import post_request, update_request

config = Config()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Celery('task', broker=config.rabbit_url, backend='rpc://')

CURRENT_DB: dict[dict, str | dict] = dict()


@app.task(bind=True)
def test(self):
    global CURRENT_DB
    # to_delete = {k: v for k, v in CURRENT_DB.items()}
    menu_id, submenu_id, dish_id = 0, 0, 0
    menu_uuid, submenu_uuid, dish_uuid = '', '', ''
    for row in reader():
        data = parser(row)
        if data.type == Types().MENU:
            menu_id = data.id
            submenu_id = 0
            dish_id = 0
            _id = f'{menu_id}.{submenu_id}.{dish_id}'
        elif data.type == Types().SUBMENU:
            submenu_id = data.id
            dish_id = 0
            _id = f'{menu_id}.{submenu_id}.{dish_id}'
        else:
            dish_id = data.id
            _id = f'{menu_id}.{submenu_id}.{dish_id}'

        # если запись есть в базе
        if _id in CURRENT_DB:
            current_data = CURRENT_DB[_id]
            if current_data['data'] != data.data:
                ids = current_data['ids']
                response = update_request(url_type=data.type, data=data.data, **ids)
                CURRENT_DB[_id]['data']['title'] = response['title']
                CURRENT_DB[_id]['data']['description'] = response['description']
                if 'price' in response:
                    CURRENT_DB[_id]['data']['price'] = response['price']
            continue

        # записи нет
        # создаем ее в базе(postgres)
        # обновляем uuid'шники
        if data.type == Types().MENU:
            menu_uuid = ''
            submenu_uuid = ''
            dish_uuid = ''
            response = post_request(url_type=data.type,
                                    data=data.data,
                                    menu_id=menu_uuid,
                                    submenu_id=submenu_uuid,
                                    dish_id=dish_uuid)
            menu_uuid = response['id']
        elif data.type == Types().SUBMENU:
            submenu_uuid = ''
            dish_uuid = ''
            response = post_request(url_type=data.type,
                                    data=data.data,
                                    menu_id=menu_uuid,
                                    submenu_id=submenu_uuid,
                                    dish_id=dish_uuid)
            submenu_uuid = response['id']
        else:
            dish_uuid = ''
            response = post_request(url_type=data.type,
                                    data=data.data,
                                    menu_id=menu_uuid,
                                    submenu_id=submenu_uuid,
                                    dish_id=dish_uuid)
            dish_uuid = response['id']

        new_data = {
            'ids': {
                'menu_id': menu_uuid,
                'submenu_id': submenu_uuid,
                'dish_id': dish_uuid
            },
            'data': data.data
        }

        CURRENT_DB[_id] = new_data
        logger.info(str(CURRENT_DB))


app.conf.beat_schedule = {
    'test_task': {
        'task': 'task.test',
        'schedule': 15,
    }
}
