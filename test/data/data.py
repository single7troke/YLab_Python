menu_create: dict = {
    'title': 'First menu',
    'description': 'First menu description'
}

menu_second_create: dict = {
    'title': 'Second menu',
    'description': 'Second menu description'
}

menu_update: dict = {
    'title': 'Updated first menu',
    'description': 'Updated first menu description'
}

menu_deleted: dict = {
    'status': True,
    'message': 'The menu has been deleted'
}

submenu_create: dict = {
    'title': 'First submenu',
    'description': 'First submenu description'
}

submenu_second_create: dict = {
    'title': 'Second submenu',
    'description': 'Second submenu description'
}


submenu_update: dict = {
    'title': 'Updated first submenu',
    'description': 'Updated first submenu description'
}

submenu_delete: dict = {
    'status': True,
    'message': 'The submenu has been deleted'
}

dish_create: dict = {
    'title': 'First dish',
    'description': 'First dish description',
    'price': '12.50'
}

dish_second_create: dict = {
    'title': 'Second dish',
    'description': 'Second dish description',
    'price': '77.99'
}

dish_third_create: dict = {
    'title': 'Third dish',
    'description': 'Third dish description',
    'price': '123.45'
}

dish_update: dict = {
    'title': 'Updated first dish',
    'description': 'Updated first dish description',
    'price': '32.69'
}

dish_delete: dict = {
    'status': True,
    'message': 'The dish has been deleted'
}


def construct_expected_resp_from_everything(data):
    result = [
        {
            'id': data['first_menu'].id,
            'title': menu_create['title'],
            'description': menu_create['description'],
            'submenus': [
                {
                    'id': data['first_sub'].id,
                    'title': submenu_create['title'],
                    'description': submenu_create['description'],
                    'dishes': [
                        {
                            'id': data['first_dish'].id,
                            'title': dish_create['title'],
                            'description': dish_create['description'],
                            'price': dish_create['price']
                        },
                        {
                            'id': data['second_dish'].id,
                            'title': dish_second_create['title'],
                            'description': dish_second_create['description'],
                            'price': dish_second_create['price']
                        }
                    ]
                }
            ]
        },
        {
            'id': data['second_menu'].id,
            'title': menu_second_create['title'],
            'description': menu_second_create['description'],
            'submenus': [
                {
                    'id': data['second_sub'].id,
                    'title': submenu_second_create['title'],
                    'description': submenu_second_create['description'],
                    'dishes': [
                        {
                            'id': data['third_dish'].id,
                            'title': dish_third_create['title'],
                            'description': dish_third_create['description'],
                            'price': dish_third_create['price']
                        },

                    ]
                }
            ]
        }
    ]
    return result
