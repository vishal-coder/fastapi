from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime, time, timedelta

from typing import Union
from .user_schemas import showUser

class project_Basic(BaseModel):   
    name:str = Field(min_length = 2, max_length = 50)    

class project_Update(BaseModel):   
    id:int
    is_completed: bool

class project(BaseModel):   
    name:str = Field(min_length = 2, max_length = 50)
    id:int
    is_completed: bool = Field(default=False)
    created_on:datetime
   
 
     
   