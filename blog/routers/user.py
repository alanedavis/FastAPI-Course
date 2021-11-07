import sys
sys.path.insert(0,'..')

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import schemas, database
from repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(db, request)

@router.get('', response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(database.get_db)):
    return user.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(database.get_db)):
    return user.get(db, id)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id, request: schemas.User, db: Session = Depends(database.get_db)):
    return user.update(db, request, id)

@router.delete('', status_code=status.HTTP_200_OK)
def delete_user(id, db: Session = Depends(database.get_db)):
    return user.delete(db, id)
