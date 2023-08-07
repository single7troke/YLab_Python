# YLab_Python
```
Kомментарий для проверяющего.
По поводу задания со * reverse
Конструктор url я реализовал еще в предыдущем ДЗ. Находится в test/core/utils.
Если url сервиса поменялся, то в тестах изменения нужно вносить только в config.py
Это естественно при условии, что логика построения нашего url не меняется.
(нам всегда нужен определенный набор id
menu - всегда нужен menu_id, кроме списка меню, там не нужно никаких id
submenu - всегда нужны menu_id и submenu_id, кроме списка подменю гда submenu_id не нужен
dish - всегда нужны menu_id, submenu_id и dish_id, кроме списка блюд где dish_id не нужен)
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
REDIS_PORT=6379" > config/dev/.env &&
cp config/dev/.env config/test
```
4. Запускаем сервис(run service).
```shell
make run
```
5. Останавливаем сервисы, удаляем контейнеры и вольюмы(Stop services, delete containers and volumes)
```shell
make stop
```
6. Запускаем тесты(run tests)Тесты можно запускать не останавливая запущенный ранее сервис, они выполняются в отдельных контейнерах.
```shell
make test_run
```
