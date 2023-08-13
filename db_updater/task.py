import logging
from typing import Any

from celery import Celery
from core import parser, reader
from core.config import Config
from core.models import Types
from core.utils import delete_request, get_hash, post_request, update_request

config = Config()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Celery('task', broker=config.rabbit_url, backend='rpc://')

HASH_SUM = None
CURRENT_DB: dict[str, Any] = dict()


@app.task(bind=True)
def test(self):
    global CURRENT_DB
    global HASH_SUM
    file_hash = get_hash(config.path_to_menu_file)
    if file_hash == HASH_SUM:
        logger.info('Nothing happened')
        return

    to_delete = {k: v for k, v in CURRENT_DB.items()}
    menu_id, submenu_id, dish_id = 0, 0, 0
    menu_uuid, submenu_uuid, dish_uuid = '', '', ''
    for row in reader():
        data = parser(row)
        if data is None:
            continue
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
                logger.info(f'Updated {current_data["type"]}, _id: {_id}')
            menu_uuid = current_data['ids']['menu_id']
            submenu_uuid = current_data['ids']['submenu_id']
            to_delete.pop(_id)
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
            logger.info(f'Created menu, _id: {_id}')
        elif data.type == Types().SUBMENU:
            submenu_uuid = ''
            dish_uuid = ''
            response = post_request(url_type=data.type,
                                    data=data.data,
                                    menu_id=menu_uuid,
                                    submenu_id=submenu_uuid,
                                    dish_id=dish_uuid)
            submenu_uuid = response['id']
            logger.info(f'Created submenu, _id: {_id}')
        else:
            dish_uuid = ''
            response = post_request(url_type=data.type,
                                    data=data.data,
                                    menu_id=menu_uuid,
                                    submenu_id=submenu_uuid,
                                    dish_id=dish_uuid)
            dish_uuid = response['id']
            logger.info(f'Created dish, _id: {_id}')

        new_data = {
            'ids': {
                'menu_id': menu_uuid,
                'submenu_id': submenu_uuid,
                'dish_id': dish_uuid
            },
            'data': data.data,
            'type': data.type,
            '_id': _id
        }

        CURRENT_DB[_id] = new_data

    for _id, data in to_delete.items():
        delete_request(url_type=data['type'], **data['ids'])
        CURRENT_DB.pop(_id)
        logger.info(f'Deleted {data["type"]}, _id: {_id}')

    HASH_SUM = file_hash
    logger.info(str(CURRENT_DB))


app.conf.beat_schedule = {
    'test_task': {
        'task': 'task.test',
        'schedule': 15,
    }
}
