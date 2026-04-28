from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.schemas.todo import Todo, TodoCreate as todoSchema
from app.api.dependencies import get_db
from ...service import todoService, userService


from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from ...service.auth import (
    create_access_token, 
    verify_password, 
    hash_password, 
    verify_token,
    oauth2_schema)

router  = APIRouter(
    prefix="/items",
    tags=["CRUD of TODO"],
    dependencies=[Depends(userService.get_user_details)] 
)

@router.post("/todos" , response_model = Todo)
def create_todo(todo: todoSchema, db:Session = Depends(get_db)):
    return todoService.create_todo(todo,db)

@router.get("/todos" , response_model=list[Todo])
def read_todos(db:Session = Depends(get_db)):
    return todoService.read_todos(db)

@router.get("/todos/{id}", response_model=Todo)
def get_todo(id : int , db:Session = Depends(get_db)):
    return todoService.get_todo(id, db)

@router.put("/todos/{id}", response_model=Todo)
def update_todo(id : int , updated :todoSchema,  db:Session = Depends(get_db)):
    return todoService.update_todo(id,updated,db)

@router.delete("/todos/{id}")
def delete_todo(id : int , db:Session = Depends(get_db)):
    return todoService.delete_todo(id,db)
