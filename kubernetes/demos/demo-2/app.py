import logging
import os

from fastapi import FastAPI
from fastapi.logger import logger

app = FastAPI()
logger.setLevel(logging.DEBUG)

COUNTER_FILE = os.environ.get("COUNTER_APP_FILEPATH", "counter.txt")


# Hello World Demo
@app.get("/")
async def index():
    logging.info("HELLO REQUEST")
    return {"message": "Hello World"}


@app.get("/healthz")
async def health():
    return {"Status": "Healthy"}


def _write_count(count: int) -> None:
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))


def _get_current_count() -> int:
    if not os.path.exists(COUNTER_FILE):
        _write_count(0)
        return 0
    with open(COUNTER_FILE) as f:
        contents = f.read()
    try:
        return int(contents)
    except ValueError:
        # Corrupt or empty file: start counting again from 0
        logger.warning("Invalid counter file %s, resetting to 0", COUNTER_FILE)
        return 0


@app.post("/counter")
async def add_counter():
    count = _get_current_count()
    _write_count(count + 1)
    return {"count": count + 1}


@app.get("/counter")
async def get_counter():
    count = _get_current_count()
    return {"count": count}
