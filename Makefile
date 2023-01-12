run-dev:
	@poetry run uvicorn --reload src.main:app

run:
	@poetry run gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app

bandit:
	@poetry run bandit -c bandit.yaml -r .src

test:
	@poetry run pytest -v --cov=src --cov-report term-missing --cov-report xml tests/
