from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from .config import settings

from . import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict()):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise cred_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise cred_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate creds",
    headers={"WWW-Authenticate": "Bearer"}      )

    token_obj = verify_access_token(token, cred_exception)
    user = db.query(models.User).filter(models.User.id==token_obj.id).first()

    return user