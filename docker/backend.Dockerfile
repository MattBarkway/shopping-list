FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get -y install libpq-dev gcc

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

RUN chmod +x init_app.sh
ENTRYPOINT ["poetry", "run", "./init_app.sh"]
