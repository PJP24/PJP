FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src/orchestrator/generated:$PYTHONPATH

COPY ./protos /app/protos

RUN python -m grpc_tools.protoc -I=/app/protos --python_out=src/orchestrator/generated --grpc_python_out=src/orchestrator/generated /app/protos/*.proto

COPY ./ .

EXPOSE 5001

CMD ["python", "main.py"]
