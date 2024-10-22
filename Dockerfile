FROM python:3.12.2

ENV PYTHONDONTWRITEBITECODE 1 #запрещаем python буферизироваться
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

COPY backend /backend
COPY test_script.sh scripts/test_run_script.sh
WORKDIR /backend
COPY .env /.env

EXPOSE 8000

RUN adduser --disabled-password task-user

USER task-user