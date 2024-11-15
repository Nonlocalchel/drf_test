#! /usr/bin/env bash

sudo -u postgres psql -d task_service_db -c "CREATE EXTENSION pg_trgm;"
python makemigrations
python manage.py migrate