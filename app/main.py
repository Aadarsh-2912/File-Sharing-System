from fastapi import FastAPI
from app.utils.database import Base, engine
from app.models import User, File, EmailVerificationToken
from app.routes import auth_router, file_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "File Sharing System API is running"}

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(file_router) 