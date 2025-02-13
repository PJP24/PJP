FROM python:3.11-slim

WORKDIR /app

COPY authentication/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY authentication /app  

EXPOSE 5000

CMD ["python", "app.py"]
