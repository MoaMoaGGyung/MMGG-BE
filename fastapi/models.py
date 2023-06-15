from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from datetime import datetime

class Boards(Base):
    __tablename__ = "boards"

    site_name = Column(String(100), index=True)
    department_id = Column(Integer, index=True)
    board_id = Column(Integer, primary_key=True, index=True)    
    board_name = Column(String(100))

class Contents(Base):
    __tablename__ = "contents"

    content_id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, index=True)
    department_id = Column(Integer, index=True)
    title = Column(String(1000))
    body = Column(Text(4294000000))
    writer_name = Column(String(100))
    click_cnt = Column(Integer)
    attach_cnt = Column(Integer)
    update = Column(DateTime(timezone=True), nullable=False, default=datetime.now)