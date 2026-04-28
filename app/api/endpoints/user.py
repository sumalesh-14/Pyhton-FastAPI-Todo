from fastapi import APIRouter, Depends
from ..schemas.user import UserCreate, UserResponse, UserUpdate, Token
from sqlalchemy.orm import Session
from ..dependencies.databaseConfig import get_db
from ...service.userService import create_user, user_update, get_users, get_token, get_user_details
from ...models.user import User

from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from ...service.auth import (
    create_access_token, 
    verify_password, 
    hash_password, 
    verify_token,
    oauth2_schema)

router = APIRouter(
    prefix = "/users",
    tags = ["user management"]
)

@router.post("/create" , response_model= UserResponse)
def create_users(userCreate : UserCreate,db: Session = Depends(get_db)):
    return create_user(userCreate,db)

@router.post("/login" , response_model= Token)
def login(
    from_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    ):
    return get_token(from_data,db)

@router.get("/me" , response_model= UserResponse)
def get_details(
    current_user = Depends(get_user_details)
):
    return current_user

from typing import Annotated

@router.put("/update", response_model=UserResponse)
def update_user(
    userUpdate: UserUpdate,
    current_user: Annotated[User, Depends(get_user_details)],
    db: Annotated[Session, Depends(get_db)],
):
    return user_update(current_user.email, userUpdate, db)

@router.get("/get", response_model=list[UserResponse])
def get_all_user(
    current_user: Annotated[User, Depends(get_user_details)],
    db: Annotated[Session , Depends(get_db)]
):
    return get_users(db)



