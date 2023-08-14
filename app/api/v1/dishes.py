from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from schemas import CreateDish, Dish
from services import DishService

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['dish'])


@router.get('',
            response_model=list[Dish],
            status_code=200,
            summary='Dish list',
            description='Returns dish list')
async def get_all_dishes(menu_id: UUID,
                         submenu_id: UUID,
                         dish: DishService = Depends(DishService)):
    dishes = await dish.list(submenu_id=submenu_id)
    return dishes


@router.get('/{dish_id}',
            response_model=Dish,
            status_code=200,
            summary='Single dish',
            description='Returns single dish')
async def get_single_dish(menu_id: UUID,
                          submenu_id: UUID,
                          dish_id: UUID,
                          dish: DishService = Depends(DishService)):
    dish = await dish.get(dish_id=dish_id)
    return dish


@router.post('',
             response_model=Dish,
             status_code=201,
             summary='New dish',
             description='Creates new dish and returns it')
async def create_dish(menu_id: UUID,
                      submenu_id: UUID,
                      body: CreateDish,
                      task: BackgroundTasks,
                      dish: DishService = Depends(DishService)):
    new_dish = await dish.create(menu_id=menu_id,
                                 submenu_id=submenu_id,
                                 data=body,
                                 task=task)
    return new_dish


@router.patch('/{dish_id}',
              response_model=Dish,
              status_code=200,
              summary='Update menu',
              description='Updates dish and returns updated dish')
async def update_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      body: CreateDish,
                      task: BackgroundTasks,
                      dish: DishService = Depends(DishService)):
    updated_menu = await dish.update(menu_id=menu_id,
                                     submenu_id=submenu_id,
                                     dish_id=dish_id,
                                     data=body,
                                     task=task)
    return updated_menu


@router.delete('/{dish_id}',
               summary='Delete dish',
               description='Deletes dish and returns message that dish have been deleted')
async def delete_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      task: BackgroundTasks,
                      dish: DishService = Depends(DishService)):
    data = await dish.delete(menu_id=menu_id,
                             submenu_id=submenu_id,
                             dish_id=dish_id,
                             task=task)
    return data
