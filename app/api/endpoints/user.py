from fastapi import APIRouter, Depends
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm import Session
from ..dependencies.databaseConfig import get_db
from ...service.userService import create_user,user_update
router = APIRouter(
    prefix = "/users",
    tags = ["user management"]
)


@router.post("/create" , response_model= UserResponse)
def create_users(userCreate : UserCreate,db: Session = Depends(get_db)):
    return create_user(userCreate,db)

@router.post("/update/{email}" , response_model= UserResponse)
def update_user(email : str ,userUpdate : UserUpdate, db : Session = Depends(get_db)):
    return user_update(email ,userUpdate, db)



