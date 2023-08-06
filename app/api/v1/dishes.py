from uuid import UUID

from fastapi import APIRouter, Depends
from schemas import CreateDish, Dish
from services import DishService

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['dish'])


@router.get('', response_model=list[Dish], status_code=200)
async def get_all_dishes(menu_id: UUID,
                         submenu_id: UUID,
                         dish: DishService = Depends(DishService)):
    dishes = await dish.list(submenu_id=submenu_id)
    return dishes


@router.get('/{dish_id}', response_model=Dish, status_code=200)
async def get_single_dish(menu_id: UUID,
                          submenu_id: UUID,
                          dish_id: UUID,
                          dish: DishService = Depends(DishService)):
    dish = await dish.get(dish_id=dish_id)
    return dish


@router.post('', response_model=Dish, status_code=201)
async def create_dish(menu_id: UUID,
                      submenu_id: UUID,
                      body: CreateDish,
                      dish: DishService = Depends(DishService)):
    new_dish = await dish.create(menu_id=menu_id, submenu_id=submenu_id, data=body)
    return new_dish


@router.patch('/{dish_id}', response_model=Dish, status_code=200)
async def update_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      body: CreateDish,
                      dish: DishService = Depends(DishService)):
    updated_menu = await dish.update(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, data=body)
    return updated_menu


@router.delete('/{dish_id}')
async def delete_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      dish: DishService = Depends(DishService)):
    data = await dish.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    return data
