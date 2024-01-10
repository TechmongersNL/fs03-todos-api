from pydantic import BaseModel

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
    user_id: int


class List(ListBase):
    tasks: list[Task] = []

    class Config:
        from_attributes = True
