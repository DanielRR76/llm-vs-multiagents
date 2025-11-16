FROM python:3.11-slim

# Instala ferramentas básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

ENV PYTHONPATH=/app
