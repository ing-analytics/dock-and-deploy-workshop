import logging
import os
import uvicorn

from fastapi import FastAPI, Request, Body
from fastapi.logger import logger
from database import get_db_conn
from sql import CREATE_USER_TABLE, INSERT_USER, SELECT_ONE, SELECT_USER

app = FastAPI()
logger.setLevel(logging.DEBUG)

@app.on_event("startup")
async def startup():
   app.state.db = get_db_conn()
   logger.info("HOORAY! APP STARTED")


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
      conn = request.app.state.db
      cursor = conn.cursor()
      cursor.execute(SELECT_ONE)
   except Exception:
      {"Status": "DB is unhealthy..."}
   return {"Status": "DB is healthy! Yey"}


@app.get("/current-user")
async def get_curr_user(request: Request):
   try:
      conn = request.app.state.db
      cursor = conn.cursor()
      cursor.execute(SELECT_USER)
      row = cursor.fetchone()
   except Exception as e:
      return {"Error": e}
   return {"Current user": row[0]}


@app.post("/current-user")
async def update_curr_user(request: Request, payload: dict = Body(...)):
   try:
      conn = request.app.state.db
      cursor = conn.cursor()
   except Exception as e:
      return {"Error": e}
   
   try:
      cursor.execute(CREATE_USER_TABLE)
   except Exception:
      logger.info("TABLE IS ALREADY CREATED")
      pass

      cursor.execute(INSERT_USER.format(user=payload["username"]))
      logger.info("New current user is set")
   return {"Status": "New Current User Set"}

if __name__ == "__main__":
   host = os.getenv("APP_HOST", "0.0.0.0")
   port = os.getenv("APP_PORT", "80")

   uvicorn.run(app, host=host, port=int(port))
