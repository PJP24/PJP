FROM python:3.11

WORKDIR /app

COPY graphql_service/requirements.txt /app/graphql_service/requirements.txt

RUN pip install --no-cache-dir -r /app/graphql_service/requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH

COPY . /app/

EXPOSE 5001

CMD ["python", "graphql_service/main.py"]