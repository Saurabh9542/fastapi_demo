from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from ..database import get_db

from .. import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
    )



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user : schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.Userout)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id :{id} does not exist")
    return user
