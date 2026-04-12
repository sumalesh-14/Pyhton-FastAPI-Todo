from datetime import datetime
from pydantic import BaseModel, EmailStr
from ..schemas.user import UserResponse

class TodoBase(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    user: UserResponse 

    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    email: EmailStr 

class Todo(TodoBase):
    id: int
    created_at: datetime
    user: UserResponse  
    class Config:
        from_attributes = True
