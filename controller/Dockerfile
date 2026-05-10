FROM python:3.12-slim-bullseye

# Instala dependências de sistema
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libpng-dev \
    libjpeg-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Configura Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

# Copia requirements primeiro (melhor para cache)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# ⚠️ CRÍTICO: Usa a porta que o Railway fornecer
EXPOSE $PORT

# Comando que usa a variável de ambiente $PORT
CMD uvicorn api.index:app --host 0.0.0.0 --port $PORT
