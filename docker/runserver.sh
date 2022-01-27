#!/bin/sh

alembic upgrade head
python -m application.initial_data
uvicorn application.asgi:application --port 80 --host 0.0.0.0
