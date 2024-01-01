from sqlalchemy.orm import Session
from ..model import models
from ..schema import project_schema
from fastapi import HTTPException,status


def create(request: project_schema.project,db: Session,current_user):
    newProject =  models.Project(name = request.name, email = current_user)
    db.add(newProject) 
    db.commit()
    db.refresh(newProject)
    return newProject

def get_all(db: Session, username):
    projects = db.query(models.Project).filter(models.Project.email == username).all()
    return projects

def getProjectByNameAndUsername(request: project_schema.project,db: Session, current_user):
    project = db.query(models.Project).filter(models.Project.name == request.name, models.Project.email == current_user ).first()
    return project

def getProjectByIDAndUsername(request: project_schema.project,db: Session, current_user):
    project = db.query(models.Project).filter(models.Project.id == request.id, models.Project.email == current_user ).one_or_none()
    if project is None:
        raise HTTPException(
        status_code=404,
        detail="Project not found",
        )
    return project

def updateProject(request: project_schema.project,db: Session,current_user):
    data = db.query(models.Project).filter(models.Project.email == current_user,
                                               models.Project.id == request.id).one_or_none()
    if data is None:
        raise HTTPException(
        status_code=404,
        detail="Project not found",
        )

    data.is_completed = request.is_completed
    db.commit()
    return True

def deleteProject(id, db: Session,current_user):
    data = db.query(models.Project).filter(models.Project.email == current_user,
                                               models.Project.id == id).one_or_none()
    if data is None:
        raise HTTPException(
        status_code=404,
        detail="Project not found",
        )

    # Delete the user
    db.delete(data)
    db.commit()
    return True

