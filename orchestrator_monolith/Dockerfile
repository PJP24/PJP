FROM python:3.12-slim

WORKDIR /app

COPY orchestrator_monolith/requirements.txt /app/orchestrator_monolith/requirements.txt

RUN pip3 install --no-cache-dir -r /app/orchestrator_monolith/requirements.txt

ENV PYTHONPATH=/app/orchestrator_monolith/src/generated:/app:$PYTHONPATH

COPY . /app/

RUN python -m grpc_tools.protoc -I=protos --python_out=orchestrator_monolith/src/generated --grpc_python_out=orchestrator_monolith/src/generated protos/*.proto

EXPOSE 8000

CMD ["python", "orchestrator_monolith/main.py"]