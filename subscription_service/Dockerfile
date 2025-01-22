FROM python:3.12

WORKDIR /app

COPY subscription_service/requirements.txt /app/subscription_service/requirements.txt

RUN pip install --no-cache-dir -r /app/subscription_service/requirements.txt

ENV PYTHONPATH=/app/subscription_service/src/grpc_services/generated:/app:$PYTHONPATH

COPY . /app/

RUN python -m grpc_tools.protoc -I=protos \
    --python_out=subscription_service/src/grpc_services/generated \
    --grpc_python_out=subscription_service/src/grpc_services/generated \
    protos/subscription.proto

EXPOSE 50052

CMD ["python3", "subscription_service/main.py"]
