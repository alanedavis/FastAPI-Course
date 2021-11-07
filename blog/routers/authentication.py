import sys
sys.path.insert(0,'..')

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database
from repository import authentication

router = APIRouter(
    prefix = '/login',
    tags = ['Authentication']
)

@router.post('')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return authentication.create(db, request)