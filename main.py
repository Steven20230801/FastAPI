from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


# 連接postgresql
try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="admin", password="admin", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connected to the database")
except Exception as e:
    print(e)


posts = [
    {"title": "Post 1", "content": "This is the content of post 1", "published": True, "rating": 4, "id": 1},
    {"title": "Post 2", "content": "This is the content of post 2", "published": False, "rating": 3, "id": 2},
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    # return all posts
    return posts


def find_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    return


def find_post_index(post_id: int):
    for i, post in enumerate(posts):
        if post["id"] == post_id:
            return i


# latest post
@app.get("/posts/latest")
def get_latest_post():
    if posts:
        return posts[-1]
    return {"error": "No posts available"}


# retrive one
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id)
    if post:
        return post
    return {"error": "Post not found"}


# create posts
@app.post("/posts")
def create_post(post: Post):
    post.id = len(posts) + 1
    posts.append(post.model_dump())
    return posts[-1]


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"messages": "from createposts"}


# @app.post("/createposts")
# def create_posts(post: Post = Body(...)):
#     return {"messages": "from createposts", "data": post.model_dump()}


@app.post("/createposts")
def create_posts(post: Post = Body(...)):
    # print each field
    return {"messages": "from createposts", "title": post.title, "content": post.content}


# delete posts
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    post = find_post(post_id)
    if post:
        posts.remove(post)
        return {"message": f"Post {post_id} has been deleted"}
    return {"error": "Post not found"}


# update posts
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    post_id = find_post_index(post_id)
    if post_id is not None:
        posts[post_id] = post.model_dump()
        return posts[post_id]
    return {"error": "Post not found"}
