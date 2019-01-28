#!/usr/bin/env bash

./wait_for_postgres.sh db:5432 -t 15
/usr/bin/python3 manage.py migrate
/usr/bin/python3 manage.py runserver 0.0.0.0:8000 &
celery -A social_network worker -l info