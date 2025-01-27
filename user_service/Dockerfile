FROM python:3.12

WORKDIR /app

COPY user_service/requirements.txt /app/user_service/requirements.txt

RUN pip install --no-cache-dir -r /app/user_service/requirements.txt

ENV PYTHONPATH=/app/user_service/src/grpc_services/generated:/app:$PYTHONPATH

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

RUN python -m grpc_tools.protoc -I=protos \
    --python_out=user_service/src/grpc_services/generated \
    --grpc_python_out=user_service/src/grpc_services/generated \
    protos/user.proto

COPY user_service/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 50051

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python3", "user_service/main.py"]
