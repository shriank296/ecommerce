DOCKER_COMMAND=docker-compose
API_NAME=api

build:
	${DOCKER_COMMAND} build

dev:
	env $(grep -v '^\s*#' docker.env | xargs) ${DOCKER_COMMAND} run --service-ports api

run_local:
	DB_URL="postgresql+psycopg2://someone:example@localhost:5432/ecommerce" SECRET_KEY=b369f3fae2281f2ceeaa271e8b694d17b72a2d45a7d586c3addd5a6fba7a76f3 uvicorn source.app.adapter.fastapi.main:app --reload --log-level debug	

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






