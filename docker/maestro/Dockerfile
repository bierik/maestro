FROM python:3.9-alpine as builder

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev


WORKDIR /app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# Backend
COPY ./api ./api
COPY ./flat ./flat
COPY ./invoice ./invoice
COPY ./maestro ./maestro
COPY ./task ./task
COPY ./customer ./customer
COPY ./authentication ./authentication
COPY ./report ./report
COPY ./manage.py ./
COPY ./docker/maestro/entrypoint.sh ./
COPY ./static ./static

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG SENTRY_DSN
ARG SOURCE_COMMIT

ENV DJANGO_SETTINGS_MODULE=maestro.settings
ENV DJANGO_CONFIGURATION=Production
ENV DJANGO_AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV DJANGO_AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV SENTRY_DSN $SENTRY_DSN
ENV SOURCE_COMMIT $SOURCE_COMMIT

RUN python manage.py collectstatic --noinput

FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --no-cache \
    postgresql-client \
    postgresql-libs

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG SENTRY_DSN
ARG SOURCE_COMMIT

ENV DJANGO_SETTINGS_MODULE=maestro.settings
ENV DJANGO_CONFIGURATION=Production
ENV DJANGO_AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV DJANGO_AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV SENTRY_DSN $SENTRY_DSN
ENV SOURCE_COMMIT $SOURCE_COMMIT

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "maestro.wsgi:application", "--bind", "0.0.0.0:8000"]
