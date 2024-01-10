from pydantic import BaseModel

# Note how this base model does not expose the password.


class UserBase(BaseModel):
    id: int
    username: str

# We allow users to sign up with username and password


class UserCreate(BaseModel):
    username: str
    password: str


class UserCredentials(BaseModel):
    username: str
    password: str

# This is the schema for the database model


class User(UserBase):
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: int
    sub: str
