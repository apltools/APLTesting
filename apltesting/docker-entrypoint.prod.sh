#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py migrate --noinput
python3 manage.py loaddata tests --noinput
python3 manage.py loaddata questions --noinput
python3 manage.py collectstatic --no-input --clear

exec "$@"
