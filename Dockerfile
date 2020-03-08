FROM python:3.8.2-slim

ARG requirements=production.txt

RUN apt-get update && apt-get install -y \
    gcc \
    apt-utils \
    libpq-dev && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/cache/* && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/ ./requirements/

RUN pip install --no-cache-dir -r requirements/$requirements

COPY project .

CMD ["python", "main.py"]