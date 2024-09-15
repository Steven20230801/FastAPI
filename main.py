from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None
    id: int = None  # id 默认为 None，服务器端生成


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
