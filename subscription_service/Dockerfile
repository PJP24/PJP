FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src/grpc_services/generated:$PYTHONPATH

RUN python -m grpc_tools.protoc -I=../protos --python_out=src/grpc_services/generated --grpc_python_out=src/grpc_services/generated ../protos/subscription.proto

CMD ["python", "main.py"]
