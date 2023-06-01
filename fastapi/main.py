from typing import Union
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, crud
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/departments/")
def read_department(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boards = crud.get_boards(db=db, skip=skip, limit=limit)
    return boards

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
# A "path" is also commonly called an "endpoint" or a "route".
# "path" is the main way to separate "concerns" and "resources".
def read_item(item_id: int, q: Union[str, None] = None):
    #Union 여러개의 타입 허용
    return {"item_id": item_id, "q": q}
