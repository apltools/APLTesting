#!/bin/sh

python3 manage.py migrate --noinput
python3 manage.py loaddata tests
python3 manage.py loaddata questions
python3 manage.py collectstatic --no-input --clear

gunicorn apltesting.wsgi -b 0.0.0.0:8007