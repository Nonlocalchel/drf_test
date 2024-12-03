FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

COPY backend /backend
WORKDIR /backend

RUN adduser --disabled-password task-user

USER task-user