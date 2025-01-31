#!/bin/bash

echo "Waiting for PostgreSQL Subs to be ready..."
until nc -z -v -w30 postgresql_subscription_service 5434; do
  echo "Waiting for PostgreSQL Subs connection..."
  sleep 5
done

echo "Creating new Alembic revision..."
alembic -c /app/notification_service/alembic.ini revision --autogenerate -m "Initial migration"

echo "Running Alembic Subs migrations..."
alembic -c /app/notification_service/alembic.ini upgrade head

echo "Starting the server..."
exec "$@"
