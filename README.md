# YLab_Python
```
Kомментарий для проверяющего.

По поводу дз-4
К сожалению был только один полноценный день(воскресенье) для выполнения это дз.
Я прекрасно понимаю, что код таски для синхронизации файла и БД выглядит ужасно.
Но цель была написать хотя бы как-то, чтоб работало.
Работа с файлом должна быть корректной
Все поля должны заполняться и быть верного типа.


Задания со *
ДЗ-2
* Реализовать вывод количества подменю и блюд для Меню через один ORM запрос. -  не выполнил в срок
** Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest
    Выполнил в срок. Тестовый сценарий test/test/test_count_of_submenus_and_dishes.py


ДЗ-3
* Описать ручки API в соответствий c OpenAPI
    Описал API средствами FastApi(summary=..., description=...)
** Реализовать в тестах аналог Django reverse() для FastAPI
    По поводу задания со * reverse
    Конструктор url я реализовал еще в предыдущем ДЗ. Находится в test/core/utils.
    Если url сервиса поменялся, то в тестах изменения нужно вносить только в config.py
    Это естественно при условии, что логика построения нашего url не меняется.
    (нам всегда нужен определенный набор id
    menu - всегда нужен menu_id, кроме списка меню, там не нужно никаких id
    submenu - всегда нужны menu_id и submenu_id, кроме списка подменю гда submenu_id не нужен
    dish - всегда нужны menu_id, submenu_id и dish_id, кроме списка блюд где dish_id не нужен)

ДЗ-4
* Обновление меню из google sheets раз в 15 сек.
    Не выполнено
** Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx
    Не выполнено

```

## Запуск
1. Копируем репозиторий(copy repo).
```shell
git clone https://github.com/single7troke/YLab_Python.git
```
2. Переходим в папку(go to directory).
```shell
cd YLab_Python
```
3. Создаем .env файл(create .env).
```shell
echo "POSTGRES_USER=user
POSTGRES_PASSWORD=1234
POSTGRES_DB=menu_db
REDIS_HOST=redis
REDIS_PORT=6379
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=pass
" > config/dev/.env &&
cp config/dev/.env config/test
```
4. Запускаем весь сервис(run service).
```shell
make run
```
5. [Переходим к описанию api](http://127.0.0.1:8000/api/openapi#/).
6. Останавливаем сервисы, удаляем контейнеры и вольюмы(Stop services, delete containers and volumes)
```shell
make stop
```

### Test
7. Зупукаем веб-сервис для тестов postman(без Celery)
```shell
make postman
```
8. Останавливаем сервисы.
```shell
make stop
```
9. Запускаем тесты(run tests)Тесты можно запускать не останавливая запущенный ранее сервис, они выполняются в отдельных контейнерах.
```shell
make test_run
```
