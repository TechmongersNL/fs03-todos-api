from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import lists, models, database, schemas, tasks

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

# get all lists


@app.get("/lists", response_model=List[schemas.List])
def read_lists(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = lists.get_lists(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results

# get alist with its tasks


@app.get("/lists/{list_id}", response_model=schemas.ListBase)
def read_list(list_id: int, db: Session = Depends(get_db)):
    results = lists.get_list(db, list_id=list_id)
    if results is None:
        raise HTTPException(status_code=404, detail="List not found")
    return results

# create list


@app.post("/lists", response_model=schemas.List)
def create_list(list: schemas.ListCreate, db: Session = Depends(get_db)):
    return lists.create_list(db, list=list)

# delete list


@app.delete("/lists", response_model=schemas.List)
def delete_lists(list_id: int, db: Session = Depends(get_db)):
    return lists.delete_list(db, list_id=list_id)


# get tasks from a list


@app.get("/lists/{list_id}/tasks", response_model=List[schemas.Task])
def read_list_tasks(list_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = tasks.get_tasks(db, list_id=list_id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return results

# create task


@app.post("/lists/{list_id}/tasks", response_model=schemas.Task)
def create_list_task(list_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return tasks.create_task(db, list_id=list_id, task=task)

# delete task


@app.delete("/lists/{list_id}/tasks", response_model=schemas.List)
def delete_list_task(list_id: int, task_id: int, db: Session = Depends(get_db)):
    return tasks.delete_task(db, list_id=list_id, task_id=task_id)
