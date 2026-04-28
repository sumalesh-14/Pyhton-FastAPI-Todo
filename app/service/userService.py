from fastapi import APIRouter, Depends, HTTPException, status
from ..api.schemas.user import UserCreate, UserResponse, UserUpdate, Token
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import User
from ..api.dependencies.databaseConfig import get_db

from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .auth import (
    create_access_token, 
    verify_password, 
    hash_password, 
    verify_token,
    oauth2_schema)
from ..config.authConfig import settings

def create_user(userCreate : UserCreate,db: Session = Depends(get_db)):
    savedUser = User(
        name=userCreate.name,
        email=userCreate.email,
        password_hash=hash_password(userCreate.password),
        role=userCreate.role
    )
    db.add(savedUser)
    db.commit()
    db.refresh(savedUser)
    return savedUser

def get_token(  
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    #get user from db
    result = db.query(User).filter( func.lower(User.email) == form_data.username.lower()).first()

    if not result or not verify_password(form_data.password, result.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Incorrect email or password")


    access_token = create_access_token(data = {"sub" : str(result.id)})

    return Token( access_token = access_token, token_type = "bearer")


def get_user_details(
    token: Annotated[str, Depends(oauth2_schema)],
    db: Annotated[Session, Depends(get_db)]
):
    user_id = verify_token(token = token)
    if user_id is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
        # Validate user_id is a valid integer (defense against malformed JWT)
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    foundUser = db.query(User).filter(User.id == user_id_int).first()

    if not foundUser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return foundUser
    
def user_update(email :str, userUpdate : UserUpdate,db: Session = Depends(get_db)):
    foundUser = db.query(User).filter(User.email == email).first()
    if not foundUser:
        raise HTTPException(status_code=404, detail= "User Not found")
    foundUser.name = userUpdate.name
    foundUser.email = userUpdate.email
    foundUser.is_active = userUpdate.is_active
    foundUser.role = userUpdate.role
    
    db.commit()
    db.refresh(foundUser)
    return foundUser

def get_users(db : Session):
    users = db.query(User).all()
    return users

