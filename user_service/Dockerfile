FROM python:3.12

WORKDIR /app

COPY user_service/requirements.txt /app/user_service/requirements.txt

RUN pip install --no-cache-dir -r /app/user_service/requirements.txt

ENV PYTHONPATH=/app/user_service/src/grpc_services/generated:/app:$PYTHONPATH

COPY . /app/

RUN python -m grpc_tools.protoc -I=protos \
    --python_out=user_service/src/grpc_services/generated \
    --grpc_python_out=user_service/src/grpc_services/generated \
    protos/user.proto

EXPOSE 50051

CMD ["python3", "user_service/main.py"]
