from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .api.schemas.todo import Todo, TodoCreate as todoSchema
from .models.todo import Todo as TodoModel
from .api.dependencies.databaseConfig import SessionLocal,Base

Base.metadata.create_all(bind=SessionLocal().get_bind())

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 #POST /todos
@app.post("/todos" , response_model = Todo)
def create_todo(todo: todoSchema, db:Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos" , response_model=list[Todo])
def read_todos(db:Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.get("/todos/{id}", response_model=Todo)
def get_todo(id : int , db:Session = Depends(get_db)):
    Todo_response = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not Todo_response:
        raise HTTPException(status_code=404 , detail= "Todo has not been found")
    return Todo_response

@app.put("/todos/{id}", response_model=Todo)
def get_todo(id : int , updated :todoSchema,  db:Session = Depends(get_db)):
    Todo_response = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not Todo_response:
        raise HTTPException(status_code=404 , detail= "Todo has not been found")
    for key,value in updated.dict().items():
        setattr(Todo_response,key,value)
    db.commit()
    db.refresh(Todo_response)  
    return Todo_response

@app.delete("/todos/{id}")
def get_todo(id : int , db:Session = Depends(get_db)):
    Todo_response = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not Todo_response:
        raise HTTPException(status_code=404 , detail= "Todo has not been found")
    db.delete(Todo_response)
    db.commit()
    return { "message" : "Todo has been deleted Sucessfully"}
