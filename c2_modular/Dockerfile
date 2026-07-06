FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    iptables curl openssl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY c2_modular/ c2_modular/
COPY CORE_SHARED/ CORE_SHARED/
COPY data/ data/

ENV PYTHONUNBUFFERED=1
ENV C2_MODULE=c2_modular

EXPOSE 9090

CMD ["python", "-m", "uvicorn", "c2_modular.gateway:app", "--host", "0.0.0.0", "--port", "9090"]
