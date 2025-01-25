dev:
	docker compose run api 

run_local:
	uvicorn source.app.adapter.fastapi.main:app --reload --log-level debug	

