FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ frontend/
COPY JOSAMICK/templates/ JOSAMICK/templates/
COPY JOSAMICK/static/ JOSAMICK/static/

ENV PYTHONUNBUFFERED=1
ENV FRONTEND_MODULE=frontend

EXPOSE 5002

CMD ["python", "frontend/server.py"]
