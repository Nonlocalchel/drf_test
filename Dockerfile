FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /temp/requirements.txt

COPY start_backend.sh /start_backend.sh
COPY backend /backend

WORKDIR /backend

RUN adduser --disabled-password task-user \
    && chown -R task-user:task-user /backend
USER task-user

ENTRYPOINT ["/start_backend.sh"]