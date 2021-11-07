import sys
sys.path.insert(0,'..')

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import schemas, database, oauth2
from repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['Blogs'],
    dependencies=[Depends(oauth2.get_current_user)]
)

@router.post('', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(db, request)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(db, request, id)

@router.delete('', status_code=status.HTTP_200_OK)
def delete_blog(id, db: Session = Depends(database.get_db)):
    return blog.delete(db, id)

@router.get('', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_blog(id, db: Session = Depends(database.get_db)):
    return blog.get(db, id)