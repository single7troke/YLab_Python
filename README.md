# YLab_Python


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
6. Запускаем тесты(run tests).
```shell
make test_run
```
