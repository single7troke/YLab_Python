FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
COPY ./ /db_updater
WORKDIR /db_updater

RUN pip install -r requirements.txt --no-cache-dir
