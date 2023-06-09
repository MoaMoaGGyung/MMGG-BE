from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
from glob import glob

DB_USER = os.environ.get("DATABASE_USERNAME")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DB_DATABASE = os.environ.get("DATABASE")
DB_HOST = os.environ.get("DATABASE_HOST")
DB_PORT = 3306

# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}"
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{}:{}@{}/{}?port={}?charset=utf8'.format(USER, PASSWORD, HOST, DATABASE, PORT)
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8'
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
except:
    sys.exit(1)
            
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()