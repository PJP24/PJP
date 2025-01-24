#!/bin/bash

KAFKA_BROKER="broker"
KAFKA_PORT=9092

echo "Waiting for Kafka to be available at $KAFKA_BROKER:$KAFKA_PORT..."
until nc -z -v -w30 $KAFKA_BROKER $KAFKA_PORT; do
  echo "Waiting for Kafka..."
  sleep 5
done

echo "Kafka is up, starting the consumer..."
exec python notification_service/consumer.py
