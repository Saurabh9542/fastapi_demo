import psycopg2
import time
from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body
from typing import Optional, List
from random import randrange
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import posts, users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


print(settings.database_password)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)




