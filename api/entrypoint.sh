#!/bin/bash
python -m celery -A api worker -l info &
python -m celery -A api beat -l info &
python /app/manage.py migrate
python /app/manage.py loaddata base.json
python /app/manage.py runserver 0.0.0.0:8000