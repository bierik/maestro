FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev


WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# Backend
COPY ./api ./api
COPY ./flat ./flat
COPY ./invoice ./invoice
COPY ./maestro ./maestro
COPY ./task ./task
COPY ./customer ./customer
COPY ./report ./report
COPY ./manage.py ./
COPY ./docker/maestro/entrypoint.sh ./
COPY ./static ./static

ENV DJANGO_SETTINGS_MODULE=maestro.settings
ENV DJANGO_CONFIGURATION=Production

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV DJANGO_AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV DJANGO_AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "maestro.wsgi:application", "--bind", "0.0.0.0:8000"]
