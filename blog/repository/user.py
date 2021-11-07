import sys
sys.path.insert(0,'..')

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
import models
from hashing import Hash

def get_all(db: Session):
    return db.query(models.User).all()

def create(db: Session, request):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update(db: Session, request, id):
    user = db.query(models.User).filter(models.User.id == id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id [{id}] does not exist')

    user.update({'name' : request.name, 'email' : request.email, 'password' : Hash.bcrypt(request.password)})
    db.commit()
    
    return 'Successfully Updated'

def delete(db: Session, id):
    user = db.query(models.User).filter(models.User.id == id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id [{id}] does not exist')

    user.delete(synchronize_session=False)
    db.commit()

    return 'Successfully Deleted'

def get(db: Session, id):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id [{id}] does not exist')

    return user