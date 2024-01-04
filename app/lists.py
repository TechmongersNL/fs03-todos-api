# app/lists.py

from sqlalchemy.orm import Session
from . import models, schemas

# get lists


def get_lists(db: Session, skip: int = 0, limit: int = 20):
    lists = db.query(models.List).offset(skip).limit(limit).all()
    print(lists)
    return lists

# create list


def create_list(db: Session, list: schemas.ListCreate):
    db_list = models.List(**list.dict())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

# delete list


def delete_list(db: Session, list_id: int):
    list = db.query(models.List).filter(models.List.id == list_id).first()
    db.delete(list)
    db.commit()
    return list

# get one list


def get_list(db: Session, list_id: int):
    list = db.query(models.List).filter(models.List.id == list_id).first()
    print(list)
    return list

# get list by name


def get_list_by_name(db: Session, name: str):
    list = db.query(models.List).filter(models.List.name == name).first()
    print(list)
    return list
