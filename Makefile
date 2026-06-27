venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

run:
	uvicorn api.server:app --reload

reset-db:
	cp api/src/db/seed.ttl api/src/db/lotr.ttl
