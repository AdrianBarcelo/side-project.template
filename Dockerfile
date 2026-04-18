FROM python:3.11.7-slim-bullseye

RUN apt-get update && rm -rf /var/lib/apt/lists/*

COPY ./scripts /app/scripts
COPY ./requirements /app/requirements

RUN pip install --no-cache-dir --disable-pip-version-check -r /app/requirements/production.txt

COPY ./src /app/src
WORKDIR /app/src

ENV DATABASE_URL=${DATABASE_URL:-postgresql+psycopg://user:password@db/db}
ENV APP_ENV=${APP_ENV:-production}

CMD bash -c "alembic upgrade head && exec uvicorn fast_api:app --host 0.0.0.0 --port 8080 --workers 4"
