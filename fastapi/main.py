from typing import Union
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, crud
import json
from glob import glob
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = {
    "http://localhost",
    "http://localhost:3000",
    "0.0.0.0:3000"
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

@app.get("/hot")
def read_posts_hot(limit: int = 10, db: Session = Depends(get_db)):
    _return_dict = []
    _contents = crud.get_hot_contents(db, limit)
    for content in _contents:
        content = content.__dict__
        _temp_dict = {
            "department": "temp_department",
            "board": "temp_board",
            'title': content["title"],
            'uploadDate': content["update"],
            'dailyFluctuation': content["click_cnt"]
        }
        _dept_dict = {
            "name": "temp",
            "id": content["department_id"]
        }
        _board_dict = {
            "name" : "temp",
            "id": content["board_id"]
        }
        _return_dict.append({"department": _dept_dict, "board": _board_dict, "post": _temp_dict})
    return _return_dict

@app.get("/department/{department_id}/board/{board_id}/content/{content_id}")
def read_detail_content_by_contentId(
        department_id: int = 1,
        board_id: int = 1,
        content_id: int = 1,
        db: Session = Depends(get_db)):
    try:
        content = crud.get_content_bycontentid(db, department_id, board_id, content_id)
    except:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Detailed Content NOT FOUND",
        )
    return content
    # for ex in content:            
    #     ex = ex.__dict__ # to dict
    #     # print(ex["content_id"])
    #     _temp_dict = {
    #         'id': ex["content_id"],
    #         'title': ex["title"],
    #         'uploadDate': ex["update"],
    #         'view': ex["click_cnt"],
    #     }
    #     # print(_content_dict)
    #     _contents_list.append(_temp_dict)
    
    # print(_contents_list)
                
    # # _contents.append(_contents_list)
    # _return_dict ={
    #     "dname": department_id, 
    #     "bname": "temp",  ## board_name
    #     "totalPage": totalPage, 
    #     "curPage": currentPage,
    #     "posts": _contents_list
    # }
        
    # return _return_dict
@app.get("/department/{department_id}/board/{board_id}")
def read_department_board_by_boardId(
        skip: int = 0, # skip page
        limit: int = 100, # page
        department_id: int = 1,
        board_id: int = 1,
        db: Session = Depends(get_db)):

    content = crud.get_contents_byid(db, board_id, (skip*limit), limit)
    content_count = len(list(crud.get_contents_byid(db, board_id, 0, 0)))
    currentPage = (skip // limit) + 1
    totalPage = (content_count // limit) + 1
    _contents_list = []
    for ex in content:            
        ex = ex.__dict__ # to dict
        # print(ex["content_id"])
        _temp_dict = {
            'id': ex["content_id"],
            'title': ex["title"],
            'uploadDate': ex["update"],
            'view': ex["click_cnt"],
        }
        # print(_content_dict)
        _contents_list.append(_temp_dict)
    
    print(_contents_list)
                
    # _contents.append(_contents_list)
    _return_dict ={
        "dname": department_id, 
        "bname": "temp",  ## board_name
        "totalPage": totalPage, 
        "curPage": currentPage,
        "posts": _contents_list
    }
        
    return _return_dict
@app.get("/department/{department_id}")
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
                'id': ex["content_id"],
                'title': ex["title"],
                'uploadDate': ex["update"],
                'view': ex["click_cnt"],
            }
            # print(_content_dict)
            _contents_list.append(_temp_dict)
        
        print(_contents_list)
                
        # _contents.append(_contents_list)
        _return_dict["boards"].append({"name": "temp", "id": board_id, "posts": _contents_list})
        
        
    # print(_contents)
    # print(_return_dict)
    # json_string = json.dumps(_return_dict, indent=4, default=str)
    return _return_dict

@app.get("/recent-posts")   
def read_recent_posts(        
        limit: int = 100,
        db: Session = Depends(get_db)):
    _return_dict = []
    _departments_id = crud.get_department_id(db)
    _departments_id =  [i[0] for i in _departments_id]
    
    for department_id in _departments_id:
        _temp_dict = {}
        # _temp_dict["department"] = {"name": "temp", "id": department_id}
        # _temp_dict["recent_posts"] = []
        _contents_list = []
        _contents = crud.get_contents_bydepartmentid(db, department_id, limit)
        for ex in _contents:            
            ex = ex.__dict__ # to dict
            # print(ex["content_id"])
            _t_dict = {
                'title': ex["title"],
                'dId': department_id,
                'bId': ex["board_id"],
                'pId': ex["content_id"]
            }
            # print(_content_dict)
            _contents_list.append(_t_dict)
            
        _temp_dict["department"] = {"name": "temp", "id": department_id}
        _temp_dict["recent_posts"] = _contents_list
        _return_dict.append(_temp_dict)
    return _return_dict
 

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/execute-sql-file")
def init_sql():
    sql_file_paths = glob('./sql/*.sql')
    print(sql_file_paths)
    _return_message = {}
    for sql in sql_file_paths:
        with open(sql, "r") as f:
            sql_queries = f.readlines()
        session = SessionLocal()
        try:
            for sql_query in sql_queries:
                sql_query.replace("\n", "")
                result = session.execute(sql_query)
            
            session.commit()
            _return_message[f"{sql.split('/')[-1]}"]= "SQL file executed successfully"
        except Exception as e:
            session.rollback()
            _return_message[f"{sql.split('/')[-1]}"]= f"SQL execution failed: {str(e)}"
        finally:
            session.close()
    
    return _return_message
            
@app.get("/remove-all-databases")
def remove_sql():
    session = SessionLocal()
    try:
        result1 = session.execute('DELETE from mmgg.boards')
        result2 = session.execute('DELETE from mmgg.contents')
        session.commit()
        return {"message": "SQL file executed successfully"}
    except Exception as e:
        session.rollback()
        return {"message": f"SQL execution failed: {str(e)}"}
    finally:
        session.close()        
        