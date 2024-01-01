from sqlalchemy.orm import Session
from ..model import models
from ..schema import task_schema
from fastapi import HTTPException,status


def create(request: task_schema.Task,db: Session,current_user):
    print("request------------------------------------",request)

    newTask =  models.Task(name = request.name, email = current_user)
    db.add(newTask) 
    db.commit()
    db.refresh(newTask)
    return newTask

def get_all(db: Session, username):
    projects = db.query(models.Task).filter(models.Task.email == username).all()
    return projects

def getTaskByNameAndUsername(request: task_schema.Task,db: Session, current_user):
    project = db.query(models.Task).filter(models.Task.name == request.name, models.Task.email == current_user ).first()
    return project

def updateProject(request: task_schema.Task,db: Session,current_user):
    print("request------------------------------------",request)
    data = db.query(models.Task).filter(models.Task.email == current_user,
                                               models.Task.id == request.id).one_or_none()
    if data is None:
        raise HTTPException(
        status_code=404,
        detail="Project not found",
        )

    data.is_completed = request.is_completed
    db.commit()
    return True

def deleteProject(id, db: Session,current_user):
    data = db.query(models.Task).filter(models.Task.email == current_user,
                                               models.Task.id == id).one_or_none()
    if data is None:
        raise HTTPException(
        status_code=404,
        detail="Project not found",
        )

    # Delete the user
    db.delete(data)
    db.commit()
    return True

