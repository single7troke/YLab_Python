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
3. Создаем .env файл
```shell
echo "POSTGRES_USER=user
POSTGRES_PASSWORD=1234
POSTGRES_DB=menu_db" > config/dev/.env
```
4. Запускаем сервис(run service).
```shell
make run
```
5. Применяем миграцию(run migration).
```shell
make alembic_migrate
```
