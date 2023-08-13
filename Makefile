.DEFAULT_GOAL := help
THIS_FILE := $(lastword $(MAKEFILE_LIST))
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

run:
	docker-compose -f config/dev/docker-compose.yml up -d

stop:
	docker-compose -f config/dev/docker-compose.yml down -v --remove-orphans

rebuild_app:
	docker image rm dev-web-app
	docker-compose -f config/dev/docker-compose.yml build

rebuild_test:
	docker image rm dev-test
	docker-compose -f config/dev/docker-compose.yml build

delete_postgres_volume:
	docker volume rm dev_menu-db

restart_app:
	docker stop dev-web-app-1
	docker start dev-web-app-1

restart_redis:
	docker stop dev-redis-1
	docker start dev-redis-1

logs_app:
	docker logs dev-web-app-1

logs_test:
	docker logs dev-test-1

alembic_init:
	docker exec -ti dev-web-app-1 alembic init -t async migrations

alembic_create_migration:
	docker exec -ti dev-web-app-1 alembic revision --autogenerate -m "init_migration"

alembic_migrate:
	docker exec -ti dev-web-app-1 alembic upgrade head

test_run:
	docker-compose -f config/test/docker-compose.yml up -d web-app db redis
	docker-compose -f config/test/docker-compose.yml up tests
	docker-compose -f config/test/docker-compose.yml down -v --remove-orphans

celery_run:
	docker-compose -f config/dev/docker-compose.yml up -d celery rabbitmq

celery_stop:
	docker-compose -f config/dev/docker-compose.yml down -v --remove-orphans celery rabbitmq

logs_celery:
	docker logs dev-celery-1

celery_image_rm:
	docker image rm dev-celery

celery_cont_rm:
	docker rm -f dev-celery-1
