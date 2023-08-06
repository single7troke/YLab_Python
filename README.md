# YLab_Python
комментарий для проверяющего.</br>
Тесты я написал для ЭНДПОИНТОВ, как было сказано в названии ДЗ.</br>
Просто дергаем ручки реквестом и смотрим что приходит в ответ.</br>
В чате было мнение что нужно сделать именно unit тесты.</br>
Если это так, то получается что задание я не выполнил.</br>

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
POSTGRES_DB=menu_db" > conf/dev/.env
```
4. Запускаем сервис(run service).
```shell
make run
```
5. Запускаем тесты(run tests).
```shell
make test_run
```
6. Останавливаем сервисы, удаляем контейнеры и вольюмы(Stop services, delete containers and volumes)
```shell
make stop
```
