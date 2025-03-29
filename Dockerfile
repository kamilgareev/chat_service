FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y mcedit nano

RUN pip install poetry

COPY . .

RUN poetry install --no-root

CMD ["sh", "-c", "poetry run uvicorn app.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000} --reload"]