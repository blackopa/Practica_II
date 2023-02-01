#!/bin/bash

if [ -z "$DEBUG" ]
then
    echo "DEBUG not found"
    python3 manage.py makemigrations
    python3 manage.py migrate
    exec python3 manage.py runserver --noreload 0.0.0.0:8080
else
    echo "DEBUG has the value: $DEBUG"
    python3 manage.py makemigrations
    python3 manage.py migrate
    exec python3 manage.py runserver 0.0.0.0:8080
fi
