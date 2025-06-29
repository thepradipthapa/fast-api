from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Response, Depends
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import session
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)



# Initialize FastAPI application
app = FastAPI()


# Database connection
# try:
#     conn = psycopg2.connect(
#         host='localhost', 
#         database='fastapi_db', 
#         user='postgres', 
#         password='postgresadmin', 
#         cursor_factory=RealDictCursor
#         )
#     cursor = conn.cursor()
#     print("Database connection was successfull!")
# except Exception as error:
#     print("Database connectin failed!")
#     print("Error :", error)
#     time.sleep(2)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Home Page!"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
