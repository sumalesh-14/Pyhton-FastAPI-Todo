from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Annotated
from datetime import datetime


class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr
    password: Annotated[str, Field(pattern="^[A-Za-z\\d@$!%*?&]{8,}$")]
    role: str = "USER"

    @field_validator("name")
    def name_validator(cls, name):
        if any(char.isdigit() for char in name):
            raise ValueError("Name should not contain numbers")
        return name
        
class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=50)]] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True