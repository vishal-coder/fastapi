from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime, time, timedelta

from typing import Union
from .user_schemas import showUser

class Task_Basic(BaseModel):   
    name:str = Field(min_length = 2, max_length = 50)
    project_id:int

class Task_Update(BaseModel):   
    id:int
    project_id:int
    is_completed: bool

class Task(BaseModel):   
    name:str = Field(min_length = 2, max_length = 50)
    id:int
    project_id:int
    is_completed: bool = Field(default=False)
    created_on:datetime
   
 
     
   