FROM python:3.9
WORKDIR /app

COPY poetry.lock poetry.toml pyproject.toml /app/
RUN pip install poetry && poetry install --no-dev

COPY src /app/src/

