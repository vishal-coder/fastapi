from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    designation = Column(String)
    password = Column(String)
    created_on = Column(DateTime(timezone=False), server_default=func.now())

    project = relationship("Project", back_populates="owner" )

    #time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Project(Base):
    __tablename__ = "projects"
    name = Column(String)   
    id = Column(Integer, primary_key=True, index=True)
    is_completed= Column(Boolean, default=False)
    owner = relationship("User", back_populates="project" )
    email = Column(String, ForeignKey('users.email'))   
    created_on = Column(DateTime(timezone=False), server_default=func.now())
    updated_on = Column(DateTime(timezone=False), onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"
    name = Column(String)   
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    is_completed= Column(Boolean, default=False)
    created_on = Column(DateTime(timezone=False), server_default=func.now())
    updated_on = Column(DateTime(timezone=False), onupdate=func.now())