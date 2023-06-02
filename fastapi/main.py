from typing import Union
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, crud
import json
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

@app.get("/posts/{department_id}")
def read_contents_by_department(
        skip: int = 0,
        limit: int = 100,
        department_id: int = 1,
        db: Session = Depends(get_db)):
    _contents = []
    _boards_id = crud.get_board_id_bydepartmentid(db, department_id)
    _boards_id = [i[0] for i in _boards_id]
    print(_boards_id)

    _return_dict = {}
    _return_dict["department"] = {"name": "temp", "id": department_id}
    _return_dict["boards"] = []
    
    for board_id in _boards_id:
        content = crud.get_contents_byid(db, board_id, skip, limit)
        _contents_list = []
        for ex in content:            
            ex = ex.__dict__ # to dict
            # print(ex["content_id"])
            _temp_dict = {
                'index': ex["content_id"],
                'title': ex["title"],
                'uploadDate': ex["update"],
                'view': ex["click_cnt"],
                'link': "temp"
            }
            # print(_content_dict)
            _contents_list.append(_temp_dict)
        
        print(_contents_list)
                
        # _contents.append(_contents_list)
        _return_dict["boards"].append({"name": "temp", "article": _contents_list})
        
        
    # print(_contents)
    # print(_return_dict)
    # json_string = json.dumps(_return_dict, indent=4, default=str)
    return _return_dict
    
    
    

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
# A "path" is also commonly called an "endpoint" or a "route".
# "path" is the main way to separate "concerns" and "resources".
def read_item(item_id: int, q: Union[str, None] = None):
    #Union 여러개의 타입 허용
    return {"item_id": item_id, "q": q}
