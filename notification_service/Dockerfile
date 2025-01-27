FROM python:3.12-slim

WORKDIR /app

COPY notification_service/requirements.txt /app/notification_service/requirements.txt

RUN pip install --no-cache-dir -r /app/notification_service/requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY notification_service/wait-for-kafka.sh /usr/local/bin/wait-for-kafka.sh

RUN chmod +x /usr/local/bin/wait-for-kafka.sh

CMD ["tail", "-f", "/dev/null"]