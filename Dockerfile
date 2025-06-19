FROM python:3.11-slim

WORKDIR /app
COPY . .

# Make sure the directory for the database exists and is writable
RUN mkdir -p /app/data && chmod 777 /app/data

ENV DB_PATH=/app/data/failures.db

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
