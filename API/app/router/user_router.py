from typing import List
from fastapi import FastAPI,APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies import get_token_header
from ..schema import user_schemas
from sqlalchemy.orm import Session
from ..utils.hashing import Hash
from datetime import  timedelta

from ..database import get_db
from  ..model import  models
from ..utils.token import create_access_token
from ..utils.oauth2 import get_current_user
from ..dbservice import userservice


router = APIRouter()

# router = APIRouter(
# prefix='/add',
# tags = ['addition']
# )

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= user_schemas.showUser)
async def create(request:user_schemas.user, db: Session = Depends(get_db)):
    print("alredyexist", request)

    alredyexist = userservice.getbyEmail(request, db)
    print("alredyexist",alredyexist)
    if alredyexist:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                            detail = f"User already exist with {request.email} email id" )
    
    hashedPassword = Hash.encryptPassword(request.password)
    newUser = userservice.create(request, db, hashedPassword)
    return newUser


@router.post("/login")
async def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = userservice.getByUsername(request, db)
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                           detail = f"username or password is incorrect")
    isPasswordCorrect = Hash.decryptPassword(request.password, user.password)
    print("isPasswordCorrect",isPasswordCorrect)

    if not isPasswordCorrect:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                           detail = f"username or password is incorrect")
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/get",  response_model=List[user_schemas.showUser]) # query parameter
async def getname(db:Session = Depends(get_db) , get_current_user: user_schemas.user = Depends(get_current_user)): # not required can be empty
    print("get_current_user^^^^^^^^^^^^^^^^^^^^^^^",get_current_user)
    return userservice.get_all(db)
    # return db.query(models.User).all()
