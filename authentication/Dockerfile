FROM python:3.11

WORKDIR /app

COPY authentication/requirements.txt /app/authentication/requirements.txt

RUN pip install --no-cache-dir -r /app/authentication/requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH

COPY . /app/

EXPOSE 8001

CMD ["python", "authentication/main.py"]