DOCKER_COMMAND=docker-compose
API_NAME=api

build:
	${DOCKER_COMMAND} build

dev:
	env $(grep -v '^\s*#' docker.env | xargs) ${DOCKER_COMMAND} run --service-ports api

run_local:
	uvicorn source.app.adapter.fastapi.main:app --reload --log-level debug	

services:
	${DOCKER_COMMAND} up -d

delete_postgres_volume:
	${DOCKER_COMMAND} down -v

db_migrate:
	${DOCKER_COMMAND} run ${API_NAME} bash -c "alembic revision --autogenerate -m \"DB migration\""

db_upgrade:
	${DOCKER_COMMAND} run ${API_NAME} bash -c "alembic upgrade head"

down:
	${DOCKER_COMMAND} down

history:
	${DOCKER_COMMAND} run ${API_NAME} bash -c "alembic history"






