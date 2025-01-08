FROM python:3.12-slim

WORKDIR /app

<<<<<<< HEAD
RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src/orchestrator/generated:$PYTHONPATH

COPY ../ .
=======
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src:$PYTHONPATH

COPY . .
>>>>>>> ede817d (Separate graphql from orchestrator)

EXPOSE 5001

CMD ["python", "main.py"]
