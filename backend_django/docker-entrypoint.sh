#!/bin/sh

echo "Waiting for MYSQL to start..."
./wait-for mysqlDB:3306

echo "Migrating the databse..."
python manage.py makemigrations
python manage.py migrate

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000