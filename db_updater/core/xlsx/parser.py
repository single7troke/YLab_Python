from typing import Any

from core.models import DataFromFile, Types


def parser(row: list) -> DataFromFile | None:
    data: dict[str, Any] = {
        'id': int,
        'type': '',
        'data': {'title': '',
                 'description': '',
                 'price': ''}
    }
    if isinstance(row[0], int):
        data['id'] = row[0]
        data['data']['title'] = row[1]
        data['data']['description'] = row[2]
        data['type'] = Types().MENU
    elif isinstance(row[1], int):
        data['id'] = row[1]
        data['data']['title'] = row[2]
        data['data']['description'] = row[3]
        data['type'] = Types().SUBMENU
    elif isinstance(row[2], int):
        data['id'] = row[2]
        data['data']['title'] = row[3]
        data['data']['description'] = row[4]
        data['data']['price'] = str(row[5])
        data['type'] = Types().DISH
    else:
        return None

    return DataFromFile(**data)
