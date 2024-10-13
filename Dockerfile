FROM python:3.12.2

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

COPY backend /backend
WORKDIR /backend

EXPOSE 8000

RUN adduser --disabled-password task-user

USER task-user