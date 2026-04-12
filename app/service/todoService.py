from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.todo import Todo, TodoCreate as todoSchema
from app.models import Todo as TodoModel
from app.api.dependencies import get_db

def create_todo(todo: todoSchema, db:Session):
    db_todo = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def read_todos(db:Session):
    return db.query(TodoModel).all()

def get_todo(id : int , db:Session):
    Todo_response = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not Todo_response:
        raise HTTPException(status_code=404 , detail= "Todo has not been found")
    return Todo_response

def update_todo(id : int , updated :todoSchema,  db:Session):
    Todo_response = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not Todo_response:
        raise HTTPException(status_code=404 , detail= "Todo has not been found")
    for key,value in updated.dict().items():
        setattr(Todo_response,key,value)
    db.commit()
    db.refresh(Todo_response)  
    return Todo_response

def delete_todo(id : int , db:Session):
    Todo_response = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not Todo_response:
        raise HTTPException(status_code=404 , detail= "Todo has not been found")
    db.delete(Todo_response)
    db.commit()
    return { "message" : "Todo has been deleted Sucessfully"}
