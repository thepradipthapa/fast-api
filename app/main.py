from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Home Page!"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
