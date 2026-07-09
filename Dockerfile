FROM python:3.13

# system dependencies

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
CMD ["sh", "-c", "echo USING DOCKERFILE && echo PORT=$PORT && uvicorn main:app --host 0.0.0.0 --port $PORT"]