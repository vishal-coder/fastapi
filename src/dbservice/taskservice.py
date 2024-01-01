from sqlalchemy.orm import Session
from ..model import models
from ..schema import task_schema
from fastapi import HTTPException,status


def create(request: task_schema.Task, db: Session,current_user):
    print("request------------------taskservice------------------", request)

    newTask = models.Task(name=request.name, project_id=request.project_id)
    db.add(newTask) 
    db.commit()
    db.refresh(newTask)
    print("request------------------taskservice------------------", newTask)

    return newTask

def get_all(project_id, db: Session,):
    projects = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    return projects

def getTaskByNameAndProjectID(request: task_schema.Task,db: Session):
    task = db.query(models.Task).filter(models.Task.name == request.name, models.Task.project_id == request.project_id).one_or_none()
    return task

def getTaskByTaskIdAndProjectID(request: task_schema.Task,db: Session):
    task = db.query(models.Task).filter(models.Task.id == request.id, models.Task.project_id == request.project_id).one_or_none()
    return task

def updateTask(request: task_schema.Task,db: Session,current_user):
    print("request------------------------------------",request)
    data = db.query(models.Task).filter(models.Task.id == request.id).one_or_none()
    if data is None:
        raise HTTPException(
        status_code=404,
        detail="Project not found",
        )

    data.is_completed = request.is_completed
    data.name = request.name
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

