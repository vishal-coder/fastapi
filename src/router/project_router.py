from typing import List
from fastapi import FastAPI,APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies import get_token_header
from ..schema import project_schema, user_schemas
from sqlalchemy.orm import Session
from ..utils.hashing import Hash
from datetime import  timedelta

from ..database import get_db
from  ..model import  models
from ..utils.token import create_access_token
from ..utils.oauth2 import get_current_user
from ..dbservice import projectservice
from ..utils.token import create_access_token
from ..utils.oauth2 import get_current_user

router = APIRouter()

# router = APIRouter(
# prefix='/add',
# tags = ['addition']
# )

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= project_schema.project)
async def create(request:project_schema.project_Basic, db: Session = Depends(get_db), current_user: user_schemas.user = Depends(get_current_user)):
    alredyexist = projectservice.getProjectByNameAndUsername(request, db,current_user)
    print("alredyexist++++++++++++++++",alredyexist)
    if alredyexist:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                            detail = f"Project already exist with {request.name} for given user" )
    
    newProject = projectservice.create(request, db,current_user)
    return newProject

@router.get("/get",  response_model=List[project_schema.project]) # query parameter
async def getname(db:Session = Depends(get_db) , current_user: user_schemas.user = Depends(get_current_user)): # not required can be empty
    return projectservice.get_all(db,current_user)
    # return db.query(models.User).all()

@router.put("/") # query parameter
async def updateProject(request:project_schema.project_Update,db:Session = Depends(get_db) , current_user: user_schemas.user = Depends(get_current_user)): # not required can be empty
    result = projectservice.updateProject(request, db,current_user)
    return {"result":result}

@router.delete("/{id}")
async def deleteProject(id: int, db:Session = Depends(get_db),current_user: user_schemas.user = Depends(get_current_user)):
    result = projectservice.deleteProject(id, db, current_user)
    return {"result":result}
