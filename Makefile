.PHONY: up down test
up:
	docker compose up --build

down:
	docker compose down -v

test:
	docker compose run --rm ingestion pytest
	docker compose run --rm retrieval pytest
