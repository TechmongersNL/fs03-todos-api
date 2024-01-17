from pydantic import BaseModel
from users.schemas import User

# task stuff


class TaskBase(BaseModel):
    id: int
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class Task(TaskBase):
    list_id: int

    class Config:
        from_attributes = True

# list stuff


class ListBase(BaseModel):
    id: int
    name: str


class ListCreate(BaseModel):
    name: str


class List(ListBase):
    tasks: list[Task] = []
    owner: User

    class Config:
        from_attributes = True
