from fastapi import FastAPI
from .api.dependencies.databaseConfig import SessionLocal, Base
from .api.endpoints import todoRouter, user, auth_sso
from starlette.middleware.sessions import SessionMiddleware
import os
import logging
from .config.loggingConfig import setup_logging

# DB table creation
Base.metadata.create_all(bind=SessionLocal().get_bind())

# Setup logging FIRST
setup_logging()

# Create logger
logger = logging.getLogger(__name__)

app = FastAPI()

# Test sensitive data filter — password should appear as ***REDACTED*** in logs
logger.info("All set for logging - %(password)s", {"password": "test@1233"})

app.include_router(todoRouter.router)
app.include_router(user.router)
app.include_router(auth_sso.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

@app.get("/fastApi")
def root():
    logger.info("Root endpoint hit")
    return {"status": "ok"}