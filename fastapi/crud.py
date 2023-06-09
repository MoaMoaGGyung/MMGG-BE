from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import models, schemas

def get_boards(db: Session, skip: int = 0, limit = 100):
    return db.query(models.Boards).offset(skip).limit(limit).all()

def get_contents(db: Session, skip: int = 0, limit = 100):
    return db.query(models.Contents).offset(skip).limit(limit).all()

def get_board_id_bydepartmentid(db: Session, department_id: int):
    return (db.query(models.Boards.board_id)
              .filter(models.Boards.department_id == department_id)
              .all())
    
def get_contents_byid(db: Session, board_id: int, skip: int =0, limit = 100):
    if limit == 0:
        return (db.query(models.Contents)
                .filter(models.Contents.board_id == board_id)
                .all())
    else:
        return (db.query(models.Contents)
                .filter(models.Contents.board_id == board_id)
                .order_by(models.Contents.update.desc())
                .offset(skip)
                .limit(limit)
                .all())
    
def get_department_id(db: Session):
    return (db.query(models.Boards.department_id)
              .distinct())
    
    
def get_contents_bydepartmentid(db: Session, department_id: int, limit = 10):
    return (db.query(models.Contents)
              .filter(models.Contents.department_id == department_id)
              .order_by(models.Contents.update.desc())
              .limit(limit=limit)
              .all())
    
def get_hot_contents(db: Session, limit = 10):
    return (db.query(models.Contents)
              .filter(models.Contents.update > datetime.utcnow() - timedelta(weeks=1) + timedelta(hours=9))
              .order_by(models.Contents.click_cnt.desc())
              .limit(limit=limit)
              .all())

def get_content_bycontentid(db:Session, departnemt_id: int, board_id: int, content_id:int):
    return (db.query(models.Contents)
              .filter(models.Contents.content_id == content_id)
              .filter(models.Contents.department_id == departnemt_id)
              .filter(models.Contents.board_id == board_id)
              .one())
    
def get_board_name_byboardid(db: Session, board_id:int):
    return (db.query(models.Boards.board_name)
              .filter(models.Boards.board_id == board_id)
              .scalar())