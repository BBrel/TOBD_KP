FROM python:3.12-alpine

WORKDIR /app/

RUN apk update && \
    apk add --no-cache gcc musl-dev linux-headers libpq-dev curl

ENV PYTHONPATH=/app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
