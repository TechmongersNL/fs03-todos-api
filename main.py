from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app import lists, models, database, schemas, tasks
from users.crud import create_user, process_login
from users.deps import get_current_user
from users.schemas import UserBase, UserCreate, UserCredentials, Token

load_dotenv()  # take environment variables from .env.

# from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# sign up users


@app.post("/users", response_model=UserBase)
def sign_up_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user=user)

# log in users


@app.post("/users/login", response_model=Token)
def login_user(user: UserCredentials, db: Session = Depends(get_db)):
    return process_login(db, user=user)


@app.post("/docslogin", response_model=Token)
def login_with_form_data(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return process_login(db, user=user)


@app.get("/users/profile", response_model=UserBase)
def get_user_profile(user: UserBase = Depends(get_current_user)):
    return user


# get all lists


@app.get("/lists", response_model=List[schemas.List])
def read_lists(
        skip: int = 0, limit: int = 20,
        user: UserBase = Depends(get_current_user),
        db: Session = Depends(get_db)):
    results = lists.get_lists(db, user_id=user.id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results

# get alist with its tasks


@app.get("/lists/{list_id}", response_model=schemas.ListBase)
def read_list(list_id: int, db: Session = Depends(get_db),
              user: UserBase = Depends(get_current_user)):
    results = lists.get_list(db, user_id=user.id, list_id=list_id)
    if results is None:
        raise HTTPException(status_code=404, detail="List not found")
    return results

# create list


@app.post("/lists", response_model=schemas.List)
def create_list(
    list: schemas.ListCreate,
    user: UserBase = Depends(get_current_user),   # get user from token
    db: Session = Depends(get_db)
):
    # create the list and pass in the user_id
    return lists.create_list(db, user_id=user.id, list=list)

# delete list


@app.delete("/lists", response_model=schemas.List)
def delete_lists(list_id: int,
                 user: UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    return lists.delete_list(db, user_id=user.id, list_id=list_id)


# get tasks from a list


@app.get("/lists/{list_id}/tasks", response_model=List[schemas.Task])
def read_list_tasks(
    list_id: int,
    user: UserBase = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    results = tasks.get_tasks(
        db, user_id=user.id, list_id=list_id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return results

# create task


@app.post("/lists/{list_id}/tasks", response_model=schemas.Task)
def create_list_task(
    list_id: int,
    task: schemas.TaskCreate,
    user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    list = lists.get_list(db, user_id=user.id, list_id=list_id)

    if list is None:
        raise HTTPException(status_code=404, detail="List not found")
    else:
        return tasks.create_task(db, list_id=list_id, task=task)

# delete task


@app.delete("/lists/{list_id}/tasks", response_model=schemas.List)
def delete_list_task(
    list_id: int,
    task_id: int,
    user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return tasks.delete_task(db, user_id=user.id, list_id=list_id, task_id=task_id)
