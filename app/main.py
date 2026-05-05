from fastapi import FastAPI
from .api.dependencies.databaseConfig import SessionLocal,Base
from .api.endpoints import todoRouter, user , auth_sso
from starlette.middleware.sessions import SessionMiddleware
import os

Base.metadata.create_all(bind=SessionLocal().get_bind())

app = FastAPI()

app.include_router(todoRouter.router)
app.include_router(user.router)
app.include_router(auth_sso.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")  # must exist in .env
)

@app.get("/fastApi")         
def root():
    return {"status": "ok"}
