from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import models, schemas

def get_boards(db: Session, skip: int = 0, limit = 100):
    return db.query(models.Boards).offset(skip).limit(limit).all()