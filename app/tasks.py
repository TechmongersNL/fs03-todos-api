# app/tasks.py

from sqlalchemy.orm import Session
from . import models, schemas

# get tasks for a specific list


def get_tasks(db: Session, list_id: int, user_id: int,
              skip: int = 0, limit: int = 20):
    tasks = db.query(models.Task).join(models.Task.list).filter(
        models.Task.list_id == list_id
    ).filter(models.List.owner_id == user_id).offset(skip).limit(limit).all()
    print(tasks)
    return tasks

# create task on a list


def create_task(db: Session, list_id: int, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump(), list_id=list_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# get one task by its id


def get_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    print(task)
    return task

# delete list


def delete_task(db: Session, list_id: int, task_id: int):
    task = db.query(models.Task).filter(
        models.List.id == list_id,
        models.Task.id == task_id
    ).first()
    db.delete(task)
    db.commit()
    return task
