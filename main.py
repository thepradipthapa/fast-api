from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time



# Initialize FastAPI application
app = FastAPI()

# Define the Post model
class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None


# Database connection
try:
    conn = psycopg2.connect(
        host='localhost', 
        database='fastapi_db', 
        user='postgres', 
        password='', 
        cursor_factory=RealDictCursor
        )
    cursor = conn.cursor()
    print("Database connection was successfull!")
except Exception as error:
    print("Database connectin failed!")
    print("Error :", error)
    time.sleep(2)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Home Page!"}

# Get all posts
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"Data": posts}

# Create a new post
@app.post("/post/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# Get a specific post by ID
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    # If post not found, raise an HTTP exception 
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!"
        )
    return {"data": post}   

# Delete a specific post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id),)
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a specific post by ID
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!"
        )
    return {"data": updated_post}