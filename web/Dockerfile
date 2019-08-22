FROM python:3.7

ENV PYTHONUNBUFFERED 1
COPY . /srv/www
WORKDIR /srv/www

RUN pip install --no-cache-dir --upgrade pip\
    && pip install --no-cache-dir poetry\
    && poetry config settings.virtualenvs.create false
