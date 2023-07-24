.DEFAULT_GOAL := help
THIS_FILE := $(lastword $(MAKEFILE_LIST))
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

run:
	docker-compose -f config/dev/docker-compose.yml up -d

stop:
	docker-compose -f config/dev/docker-compose.yml --remove-orphans

build:
	docker image rm dev-web-app
	docker-compose -f config/dev/polling.yml build

delete_postgres_volume:
	docker volume rm dev_menu-db

restart_app:
	docker stop dev-web-app-1
	docker start dev-web-app-1

app_logs:
	docker logs dev-web-app-1

alembic_init:
	docker exec -ti dev-web-app-1 alembic init -t async migrations

alembic_create_migration:
	docker exec -ti dev-web-app-1 alembic revision --autogenerate -m "init_migration"

alembic_migrate:
	docker exec -ti dev-web-app-1 alembic upgrade head