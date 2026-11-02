FROM python:3.14-slim

# PYTHONDONTWRITEBYTECODE: don't write .pyc files into the image
# PYTHONUNBUFFERED: print logs immediately (no buffering), so `docker logs` shows them
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/web

# Copy requirements.txt on its own first: Docker caches this layer, so
# dependencies are only reinstalled when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as a non-root user
RUN groupadd --gid 1000 pokemon \
    && useradd --uid 1000 --gid pokemon --create-home pikachu
USER pikachu

EXPOSE 5001

CMD ["python", "web.py"]
