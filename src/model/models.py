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

    #time_updated = Column(DateTime(timezone=True), onupdate=func.now())

