FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src/orchestrator/generated:$PYTHONPATH

COPY ../ .

EXPOSE 5001

CMD ["python", "main.py"]