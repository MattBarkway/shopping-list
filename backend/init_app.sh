#!/bin/sh

python create_schema.py
alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 8080

exec "$@"
