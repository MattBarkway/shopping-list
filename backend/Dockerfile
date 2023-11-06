FROM python:3.10.4-slim

WORKDIR /app

RUN apt-get update && apt-get -y install libpq-dev gcc curl

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN poetry add psycopg2

RUN poetry lock --no-update

COPY . .

EXPOSE 8000

RUN chmod +x init_app.sh
ENTRYPOINT ["./init_app.sh"]
