from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Response, Depends

from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import session


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

# Get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    post = db.query(models.Post).all()
    return post


# Create a new post
@app.post("/post/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a specific post by ID
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # If post not found, raise an HTTP exception 
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!"
        )
    return post

# Delete a specific post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id),)
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a specific post by ID
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()



@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user