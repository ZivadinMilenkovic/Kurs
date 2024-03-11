from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import get_db
from . import schemas
from . import utils
from .routers import user, post, auth

# makes new table that we define in model

model.Base.metadata.create_all(bind=engine)

# declaring type of crypting algorithm

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("database connection wasa succesfull")
        break
    except Exception as error:
        print("connecting to database fail")
        print("Error", error)
        time.sleep(2)


@app.get("/")
def hello():
    return {"message": "Welcom to my API"}
