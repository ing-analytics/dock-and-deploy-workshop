FROM python:3.14-slim

# PYTHONDONTWRITEBYTECODE: don't write .pyc files into the image
# PYTHONUNBUFFERED: print logs immediately (no buffering), so `kubectl logs` shows them
# COUNTER_APP_FILEPATH: where app.py stores the counter (the deployment mounts a volume here)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    COUNTER_APP_FILEPATH=/app/counter/counter.txt

WORKDIR /app

# Copy requirements.txt on its own first: Docker caches this layer, so
# dependencies are only reinstalled when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Run as a non-root user. It needs write access to the counter directory.
RUN groupadd --gid 1000 pokemon \
    && useradd --uid 1000 --gid pokemon --create-home pikachu \
    && mkdir /app/counter \
    && chown pikachu:pokemon /app/counter
USER pikachu

EXPOSE 8080

CMD ["fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "8080"]
