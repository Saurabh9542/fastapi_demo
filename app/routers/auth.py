from fastapi import APIRouter, Depends, HTTPException, status, responses
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import schemas, models, utils, oath, schemas
from ..database import get_db

router = APIRouter(
    tags=["Auth"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==user_cred.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid crediantials")
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid crediantials")
    
    access_token = oath.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token,"token_type": "bearer"}