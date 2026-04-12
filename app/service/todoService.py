from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.todo import Todo, TodoCreate as todoSchema
from app.models import Todo as TodoModel
from app.models import User as UserModel
from app.api.dependencies import get_db

def create_todo(todo: todoSchema, db: Session):

    print("creating the todo")

    founduser = db.query(UserModel).filter(UserModel.email == todo.email).first()

    if not founduser:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db_todo = TodoModel(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user=founduser
        )

        db.add(db_todo)

        db.flush()  # 🔥 get ID without commit

        print(f"Generated ID = {db_todo.id}")

        # 🔥 business validation
        if db_todo.id == 4:
            raise HTTPException(status_code=400, detail="Invalid todo condition")

        db.commit()  # ✅ commit ONLY if everything is fine

        db.refresh(db_todo)

        return db_todo

    except Exception as e:
        db.rollback()  # 🔁 rollback if ANY error
        print("Transaction rolled back")
        raise e

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
