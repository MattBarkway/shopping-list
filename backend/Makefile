#export PYTHONPATH := .

install:
	poetry install;

runserver:
	 uvicorn main.app:app --host 0.0.0.0 --reload

install_hooks:
	poetry install; \
	pre-commit install; \

run_hooks:
	pre-commit run --all-files

style:
	poetry run ruff .

types:
	poetry run mypy .

format:
	black main --check

lint:
	flake8 main && isort main --diff && black main --check && mypy --namespace-packages -p "main" --config-file setup.cfg

migration:
	# e.g.: make m="my message" migration
	poetry run alembic revision --autogenerate -m "$(m)"

migrate:
	poetry run alembic upgrade head

docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_start:
	docker-compose start

docker_down:
	docker-compose down

docker_remove_dangling_images:
	docker images --filter "dangling=true" -q --no-trunc | xargs docker rmi