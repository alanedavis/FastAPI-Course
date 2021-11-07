import sys
sys.path.insert(0,'..')

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from hashing import Hash
import models, jwt

def create(db: Session, request):
    print(request.username)
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the email [{request.username}] does not exist')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect Password')

    access_token = jwt.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}