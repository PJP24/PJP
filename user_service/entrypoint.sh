#!/bin/bash
echo "Waiting for PostgreSQL User to be ready..."
until nc -z -v -w30 postgresql_user_service 5432; do
  echo "Waiting for PostgreSQL User connection..."
  sleep 5
done

echo "Running Alembic User migrations..."
alembic -c user_service/alembic.ini upgrade head

echo "Starting the server..."
exec "$@"
