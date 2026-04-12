from fastapi import FastAPI
from .api.dependencies.databaseConfig import SessionLocal,Base
from .api.endpoints import todoRouter, user 

Base.metadata.create_all(bind=SessionLocal().get_bind())

app = FastAPI()

app.include_router(todoRouter.router)
app.include_router(user.router)


@app.get("/fastApi")         
def root():
    return {"status": "ok"}
