from sqlalchemy.orm import Session
from ..model import models
from ..schema import user_schemas
from fastapi import HTTPException,status

def get_all(db: Session):
    users = db.query(models.User).all()
    return users

def getByUsername(request: user_schemas.user,db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    return user

def getbyEmail(request: user_schemas.user,db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    return user


def create(request: user_schemas.user,db: Session, hashedPassword:str):
    newUser =  models.User(name = request.name, email = request.email,
                           designation = request.designation,
                           password = hashedPassword)
    db.add(newUser) 
    db.commit()
    db.refresh(newUser)
    return newUser
