from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from ..schema.user_schemas import TokenData 
SECRET_KEY = "e844d87462ff21a3e693abd3ccd6f6f6e6a6695c58bb8bd25df6edcc3165c110"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return username
    except JWTError:
        raise credentials_exception
