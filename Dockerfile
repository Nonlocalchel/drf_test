FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /temp/requirements.txt

COPY start_backend.sh /usr/local/bin/start_backend.sh
RUN chmod +x /usr/local/bin/start_backend.sh

ENV HOME=/home/task_app
ENV APP_HOME=/home/task_app/backend

RUN mkdir $HOME \
    && mkdir $APP_HOME \
    && mkdir $HOME/static

COPY backend $APP_HOME
WORKDIR $APP_HOME

RUN adduser --disabled-password task-user \
    && chown -R task-user:task-user $APP_HOME \
    && chown -R task-user:task-user $HOME/static

USER task-user

ENTRYPOINT ["start_backend.sh"]