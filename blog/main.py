from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.param_functions import Body
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
# import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Blog with the id [{id}] does not exist')

    blog.update(request.dict())
    db.commit()
    return 'Successfully Updated'

@app.delete('/blog', status_code=status.HTTP_200_OK)
def remove(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Blog with the id [{id}] does not exist')

    blog.delete(synchronize_session=False)
    db.commit()
    return 'Successfully removed'

@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

@app.get('/blog/{id}', status_code=HTTP_200_OK)
def show_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Blog with the id [{id}] does not exist')

    return blog


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=9000)