from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # only get a certain amount of published blogs
    if published:
        return {'data' : f'{limit} published blog list from database'}
    else:
        return {'data' : f'{limit} blog list from database'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data' : 'all unpublished'}

@app.get('/blog/{id}')
def about(id: int):
    # fetch blog with id = id
    return {'data' :  id}

@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    # fetch comments of blog with id = id
    return {'data' : {'1', '2'}}

class Blog(BaseModel):
    # creates prototype for blog object
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    # return blog, request body
    return {'data' : f"Blog is created with title as {request.title}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)