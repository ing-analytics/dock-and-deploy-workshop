import logging
import os
import uvicorn

from fastapi import FastAPI, Request, Body
from fastapi.logger import logger
from contextlib import asynccontextmanager
from database import get_db_conn
from sql import CREATE_USER_TABLE, INSERT_USER, SELECT_ONE, SELECT_USER

logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
   logger.info("HOORAY! APP STARTED")
   # We connect to the database on the first request (see get_db below)
   app.state.db = None
   yield
   if app.state.db is not None:
      app.state.db.close()

app = FastAPI(lifespan=lifespan)


def get_db(request: Request):
   """Return the database connection. Connect (again) if we are not connected.

   This way the app also works if the database starts after the app,
   or restarts while the app is running.
   """
   conn = request.app.state.db
   if conn is None or conn.closed:
      conn = get_db_conn()
      if conn is None:
         raise RuntimeError("Not connected to the database, see the app logs")
      conn.cursor().execute(CREATE_USER_TABLE)
      request.app.state.db = conn
   return conn


# Hello World Demo
@app.get("/hello")
async def index():
   logger.info("HELLO REQUEST")
   return {"message": "Hello World"}


@app.get("/healthz")
async def health():
   return {"Status": "Healthy"}


# With Database
@app.get("/db-health")
async def db_health(request: Request):
   try:
      cursor = get_db(request).cursor()
      cursor.execute(SELECT_ONE)
   except Exception:
      return {"Status": "DB is unhealthy..."}
   return {"Status": "DB is healthy! Yey"}


@app.get("/current-user")
async def get_curr_user(request: Request):
   try:
      cursor = get_db(request).cursor()
      cursor.execute(SELECT_USER)
      row = cursor.fetchone()
   except Exception as e:
      return {"Error": str(e)}
   return {"Current user": row[0] if row else None}


@app.post("/current-user")
async def update_curr_user(request: Request, payload: dict = Body(...)):
   if "username" not in payload:
      return {"Error": "username is missing"}
   try:
      cursor = get_db(request).cursor()
      cursor.execute(INSERT_USER, (payload["username"],))
   except Exception as e:
      return {"Error": str(e)}
   logger.info("New current user is set")
   return {"Status": "New Current User Set"}

if __name__ == "__main__":
   host = os.getenv("APP_HOST", "0.0.0.0")
   port = os.getenv("APP_PORT", "8000")

   uvicorn.run(app, host=host, port=int(port))
