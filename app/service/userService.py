from fastapi import APIRouter, Depends, HTTPException
from ..api.schemas.user import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm import Session
from ..models import User
from ..api.dependencies.databaseConfig import get_db

def create_user(userCreate : UserCreate,db: Session = Depends(get_db)):
    savedUser = User(
        name=userCreate.name,
        email=userCreate.email,
        password=userCreate.password,
        role=userCreate.role
    )
    db.add(savedUser)
    db.commit()
    db.refresh(savedUser)
    return savedUser

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


