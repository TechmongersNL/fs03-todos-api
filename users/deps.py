from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from pydantic import ValidationError
from app import database
from users import model
from users.schemas import TokenPayload, UserBase
from users.credentials import ALGORITHM, JWT_SECRET_KEY

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/docslogin",  # only for usage in the docs!
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserBase:
    try:
        db = database.SessionLocal()

        # token here comes from the Authorization header and is always present
        # if we reach this code
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    [user_id, _username] = token_data.sub.split(":")
    user = db.query(model.User).filter(model.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
        )

    return user
