from pydantic import BaseModel, Field
from uuid import UUID

class Project(BaseModel):
    id:UUID
    name:str = Field(min_length = 2, max_length = 50)
    user_id:int = Field(gt = 0 )
    created_date:str
    modified_date:str
    is_completed:bool