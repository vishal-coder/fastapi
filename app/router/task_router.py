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
    taskservice.create(request, db, current_user)
    return {"result": True}

@router.get("/{project_id}",  response_model=List[task_schema.Task]) # query parameter
async def getAll(project_id:int, db:Session = Depends(get_db) , current_user: user_schemas.user = Depends(get_current_user)):
    alredyexist = projectservice.getProjectByIDAndUsername(project_id, db, current_user)
    if not alredyexist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Project does not exist with {project_id} for given user")

    list = taskservice.get_all(project_id, db)
    print("request-----------list--------------------------", list)

    return {"data" : list}


@router.put("/") # query parameter
async def updateTask(request:task_schema.Task_Update, db:Session = Depends(get_db) , current_user: user_schemas.user = Depends(get_current_user)):
    alredyexist = projectservice.getProjectByIDAndUsername(request.project_id, db, current_user)
    if not alredyexist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project does not exist with {request.project_id} for given user")


    alreadyTask = taskservice.getTaskByTaskIdAndProjectID(request, db)
    if not alreadyTask:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task does not exist with id {request.id} for given project or user")

    result = taskservice.updateTask(request, db, current_user)
    taskList = taskservice.get_all(request.project_id, db)
    print("request-----------list--------------------------", taskList)

    # to check if remaining task status is complete or not
    # if complete then update status of project as completed
    all_completed = all(task.is_completed == True for task in taskList)
    if all_completed:
        print("Completed")
        request.id = request.project_id
        request.is_completed = True
        result = projectservice.updateProject(request, db, current_user)
    return {"result":result}

@router.delete("/")
async def deleteTask(request:task_schema.Task_Update, db:Session = Depends(get_db),current_user: user_schemas.user = Depends(get_current_user)):
    alredyexist = projectservice.getProjectByIDAndUsername(request.project_id, db, current_user)
    if not alredyexist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project does not exist with {request.project_id} for given user")


    alreadyTask = taskservice.getTaskByTaskIdAndProjectID(request, db)
    if not alreadyTask:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task does not exist with id {request.id} for given project or user")

    result = taskservice.deleteTask(request.id, db)

    # to check if remaining task status is complete or not
    # if complete then update status of project as completed
    taskList = taskservice.get_all(request.project_id, db)
    print("request-----------list--------------------------", taskList)
    all_completed = all(task.is_completed == True for task in taskList)
    if all_completed:
        print("Completed")
        request.id = request.project_id
        request.is_completed = True
        result = projectservice.updateProject(request, db, current_user)

    return {"result":result}
