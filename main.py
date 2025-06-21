from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(
        host='localhost', 
        database='fastapi_db', 
        user='postgres', 
        password='postgresadmin', 
        cursor_factory=RealDictCursor
        )
    cursor = conn.cursor()
    print("Database connection was successfull!")
except Exception as error:
    print("Database connectin failed!")
    print("Error :", error)
    time.sleep(2)

posts = [
    {"id": 1, "title": "Exploring FastAPI", "content": "FastAPI is a modern web framework for building APIs with Python."},
    {"id": 2, "title": "Django Tips", "content": "Use class-based views for reusable and modular code."},
    {"id": 3, "title": "JWT Authentication", "content": "JWT allows secure transmission of information between parties as JSON objects."},
    {"id": 4, "title": "Intro to Prompt Engineering", "content": "Prompt engineering helps control and guide large language models effectively."},
    {"id": 5, "title": "Deploy with Netlify", "content": "You can host static websites quickly with Netlify and custom domains."}
]


def find_post(id):
    for p in posts:
        if p['id']==id:
            return p 
def find_index_post(id):
    for i,p in enumerate(posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to the Home Page!"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"Data": posts}

@app.post("/post/")
def create_posts(post: Post):
    return post


@app.get("/posts/{id}")
def get_post(id: int):
    post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found!")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Post with id: {id} not found!")
    posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Post with id: {id} not found!")
    post_dict = post.dict()
    post_dict['id']=id
    posts[index]=post_dict
    return {"data": post_dict}