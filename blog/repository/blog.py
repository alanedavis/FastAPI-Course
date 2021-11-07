import sys
sys.path.insert(0,'..')

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
import models

def get_all(db: Session):
    return db.query(models.Blog).all()

def create(db: Session, request):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def update(db: Session, request, id):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id [{id}] does not exist')

    blog.update(request.dict())
    db.commit()

    return 'Successfully Updated'

def delete(db: Session, id):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id [{id}] does not exist')

    blog.delete(synchronize_session=False)
    db.commit()

    return 'Successfully removed'

def get(db: Session, id):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id [{id}] does not exist')

    return blog