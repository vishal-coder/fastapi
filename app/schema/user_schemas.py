from pydantic import BaseModel, EmailStr, Field
from typing import Union

class user(BaseModel):
    name:str
    designation:str
    email:EmailStr
    password:str

class showUser(BaseModel):
    name:str
    designation:str
    email:str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None