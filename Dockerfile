FROM python:3.7-alpine

RUN apk add gcc make musl-dev libffi-dev libressl-dev libpq postgresql-dev
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install

COPY . .

CMD ["python", "run.py"]
