FROM python:3.14-slim

# PYTHONDONTWRITEBYTECODE: don't write .pyc files into the image
# PYTHONUNBUFFERED: print logs immediately (no buffering), so `docker logs` shows them
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000

WORKDIR /app

# Copy requirements.txt on its own first: Docker caches this layer, so
# dependencies are only reinstalled when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

# Run as a non-root user
RUN groupadd --gid 1000 pokemon \
    && useradd --uid 1000 --gid pokemon --create-home pikachu
USER pikachu

# Documents the port the app listens on (publish it with `docker run -p`)
EXPOSE 8000

# main.py reads APP_HOST and APP_PORT and starts uvicorn
CMD ["python", "main.py"]
