# FastAPI mailing lists system

An example of FastAPI backend with a mailing lists system

## Project setup

### Development

```shell script
poetry install

docker-compose up -d db redis mailhog
alembic upgrade head
# initial data (first superuser)
python -m application.initial_data
# backend
python -m application.asgi
```

### Docker

```shell script
docker-compose up -d app
```

## API documentation

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)