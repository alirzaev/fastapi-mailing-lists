FROM python:3.9-slim
EXPOSE 80

WORKDIR /usr/src/project

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

RUN chmod +x ./docker/wait-for-it.sh
RUN chmod +x ./docker/runserver.sh

CMD ["./docker/runserver.sh"]