FROM python:3.11-alpine as builder

WORKDIR /srv/www/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements_linux.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /srv/www/backend/wheels -r requirements_linux.txt


FROM python:3.11-alpine

WORKDIR /srv/www/backend

COPY --from=builder  /srv/www/backend/wheels /wheels
COPY . .

RUN pip install --no-cache /wheels/*
