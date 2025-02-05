#!/bin/bash
echo "Waiting for PostgreSQL User to be ready..."
until nc -z -v -w30 postgresql_user_service 5432; do
  echo "Waiting for PostgreSQL User connection..."
  sleep 5
done


echo "Creating new Alembic revision..."
alembic -c /app/user_service/alembic.ini revision --autogenerate -m "Update User model"


echo "Running Alembic User migrations..."
alembic -c /app/user_service/alembic.ini upgrade head

echo "Starting the server..."
exec "$@"
