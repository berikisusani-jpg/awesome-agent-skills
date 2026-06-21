FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    libjack-jackd2-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run FastAPI by default
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
