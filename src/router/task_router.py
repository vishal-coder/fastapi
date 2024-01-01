from typing import List
from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dbservice import projectservice
from ..dependencies import get_token_header
from ..schema import task_schema, user_schemas
from sqlalchemy.orm import Session
from ..utils.hashing import Hash
from datetime import timedelta

from ..database import get_db
from ..model import models
from ..utils.token import create_access_token
from ..utils.oauth2 import get_current_user
from ..dbservice import projectservice, taskservice
from ..utils.token import create_access_token
from ..utils.oauth2 import get_current_user

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: task_schema.Task_Basic, db: Session = Depends(get_db),
                 current_user: user_schemas.user = Depends(get_current_user)):

    alredyexist = projectservice.getProjectByIDAndUsername(request.project_id, db, current_user)
    if not alredyexist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Project does not exist with {request.name} for given user")

    alreadyTask = taskservice.getTaskByNameAndProjectID(request, db)
    if alreadyTask:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                            detail=f"Task already exist with name {request.name} for given project" )
    print("request-----------alreadyTask--------------------------", alreadyTask)
    taskservice.create(request, db, current_user)
    return {"result": True}

# @router.get("/get",  response_model=List[task_schema.project]) # query parameter
# async def getname(db:Session = Depends(get_db) , current_user: user_schemas.user = Depends(get_current_user)): # not required can be empty
#     return taskservice.get_all(db,current_user)
#     # return db.query(models.User).all()

# @router.put("/") # query parameter
# async def updateProject(request:task_schema.project_Update,db:Session = Depends(get_db) , current_user: user_schemas.user = Depends(get_current_user)): # not required can be empty
#     result = taskservice.updateProject(request, db,current_user)
#     return {"result":result}

# @router.delete("/{id}")
# async def deleteProject(id: int, db:Session = Depends(get_db),current_user: user_schemas.user = Depends(get_current_user)):
#     result = taskservice.deleteProject(id, db, current_user)
#     return {"result":result}
