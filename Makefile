.PHONY: setup up down logs bot shell psql test lint fmt reset-db

setup:           ## pierwszy start: tworzy .env i buduje obrazy
	python scripts/setup_env.py
	docker compose build

up:              ## baza + bot w tle
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f bot

bot:             ## tylko baza w Dockerze, bot lokalnie z venv
	docker compose up -d db
	python -m methin

shell:
	docker compose run --rm bot bash

psql:
	docker compose exec db sh -c "psql -U $$POSTGRES_USER -d $$POSTGRES_DB"

test:            ## testy w kontenerze (wymaga działającej bazy)
	docker compose up -d db
	docker compose run --rm bot pytest -q

lint:
	docker compose run --rm bot ruff check src tests

fmt:
	docker compose run --rm bot ruff format src tests

reset-db:        ## USUWA wszystkie dane deweloperskie
	docker compose down -v
	docker compose up -d db
