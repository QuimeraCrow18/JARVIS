FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 net-tools && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY brain_core/ brain_core/
COPY CORE_SHARED/ CORE_SHARED/
COPY JOSAMICK/ JOSAMICK/
COPY scripts/ scripts/

ENV PYTHONUNBUFFERED=1
ENV BRAIN_MODULE=brain_core

EXPOSE 5001

CMD ["python", "brain_core/runner.py"]
