from sqlalchemy.orm import Session
from fastapi import HTTPException, status

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
    return (db.query(models.Contents)
              .filter(models.Contents.board_id == board_id)
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
              .order_by(models.Contents.click_cnt.desc())
              .limit(limit=limit)
              .all())
    