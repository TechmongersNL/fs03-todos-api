from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import model, schemas
from .credentials import (
    create_access_token,
    get_hashed_password,
    verify_password
)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = model.User(username=user.username, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def process_login(db: Session, user: schemas.UserCredentials):
    db_user = db.query(model.User).filter(
        model.User.username == user.username).first()

    user_password_error = "Incorrect username or password"

    if db_user is None:
        raise HTTPException(status_code=404, detail=user_password_error)

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail=user_password_error)

    return {
        "access_token": create_access_token(
            f"{db_user.id}:{db_user.username}"
        ),
        "token_type": "bearer"
    }
