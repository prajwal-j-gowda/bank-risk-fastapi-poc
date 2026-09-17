FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fastapi_app.py .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn fastapi_app:app --host 0.0.0.0 --port ${PORT:-8000}"]
