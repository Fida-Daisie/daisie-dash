from sqlalchemy import Table, schema
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from ..database.db import db_alchemy
import pandas as pd

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table

engine = db_alchemy(name='database').get_engine()



from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'user'

    id=Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    

    def __init__(self, id, name, email):
        self.id = id
        self.name = name 
        self.email = email
        

    @staticmethod
    def get(id):
        user_id =id
        users = pd.read_sql_table('user', schema='admin', con=engine)
        
        user_id = str(user_id)
        user_df = users[users['id'] ==user_id]
        
        if user_df.shape[0] == 0:
            return None
        else:
            user = User(
                id=user_df.iloc[0,0], name=user_df.iloc[0,1], email=user_df.iloc[0,2]
            )
        return user

    @staticmethod
    def create(id, name, email):
        insertion_object_2 = [str(id), name, email]
        engine.execute("INSERT INTO admin.user (id, name, email) VALUES (%s, %s, %s)" , insertion_object_2) 

