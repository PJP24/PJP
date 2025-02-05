#!/bin/bash

echo "Waiting for PostgreSQL Subs to be ready..."
until nc -z -v -w30 postgresql_subscription_service 5433; do
  echo "Waiting for PostgreSQL Subs connection..."
  sleep 5
done

echo "Creating new Alembic revision..."
alembic -c /app/subscription_service/alembic.ini revision --autogenerate -m "Automatic migration for model changes"

echo "Running Alembic Subs migrations..."
alembic -c /app/subscription_service/alembic.ini upgrade head

echo "Starting the server..."
exec "$@"
