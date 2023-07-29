FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
COPY ./ /test
WORKDIR /test

RUN pip install -r requirements.txt --no-cache-dir
