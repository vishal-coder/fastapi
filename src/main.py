from typing import Union, Optional
from fastapi import FastAPI, HTTPException, Depends, status
# from .src.router import user_router
from .router import user_router, project_router, task_router
from .utils.oauth2 import get_current_user
from .database import  engine
from .model import  models
from .schema import  user_schemas
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(
    user_router.router,
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
)

app.include_router(
    project_router.router,
    prefix="/project",
    tags=["project"],
    # dependencies=[user_id:=Depends(auth.oauth2_scheme)]
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
)

app.include_router(
    task_router.router,
    prefix="/task",
    tags=["Task"],
    # dependencies= [current_user: user_schemas.user = Depends(get_current_user)]
    # dependencies=[Depends(get_token_header)],

)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}





# @app.get("/getproject/{id}")  # path paramter
# def getStudent(id: int):
#     return {"id":id}

# @app.get("/getname") # query parameter
# async def getname(name: Optional[str] = None): # not required can be empty
#     return {"name is":name}

# @app.post("/createproject")
# async def createproject(project:Project):
#     #  raise HTTPException(
#     #      status_code:404,
#     #      details = f"ID{Project} not found"
#     #  )
#      return {"project":project }