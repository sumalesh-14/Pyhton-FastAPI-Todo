from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.schemas.todo import Todo, TodoCreate as todoSchema
from app.api.dependencies import get_db
from ...service import todoService

router  = APIRouter(
    prefix="/items",
    tags=["CRUD of TODO"]
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
