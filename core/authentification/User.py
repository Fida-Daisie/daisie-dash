from sqlalchemy import Table, schema
# from sqlalchemy.sql import select
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash
from ..database.db import db_alchemy
import pandas as pd

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, MetaData, inspect

from flask_login import UserMixin
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'user'

    engine = db_alchemy(name='database').get_engine()

    id = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    
    alt_user_df = pd.DataFrame(columns=["id", "name", "email"]) # use only if not DB available 

    def __init__(self, id, name, email):
        self.id = id
        self.name = name 
        self.email = email
        
        try:
            if not inspect(User.engine).has_table('user'):  # If table don't exist, Create.
                metadata = MetaData(User.engine, schema='admin') # TODO Create schema if necessary
                Table('user', metadata,
                    Column('id', String, primary_key=True, nullable=False), 
                    Column('name', String), 
                    Column('email', String)
                )     
                metadata.create_all()
        except Exception as e:
            print("No database for Users available\nUse intrinsic dataframe instead\n"+str(e))

    @staticmethod
    def get(user_id):
        try:
            users = pd.read_sql_table('user', schema='admin', con=User.engine)
        except Exception as e:
            print("No database for Users available\nUse intrinsic dataframe instead\n"+str(e))
            users = User.alt_user_df.copy()
        
        user_id = str(user_id)
        user_df = users[users['id'] == user_id]
        
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
        try:
            User.engine.execute("INSERT INTO admin.user (id, name, email) VALUES (%s, %s, %s)" , insertion_object_2)
        except Exception as e:
            print("No database for Users available\nUse intrinsic dataframe instead\n"+str(e))
            User.alt_user_df = pd.concat(
                [
                    User.alt_user_df, 
                    pd.DataFrame([insertion_object_2], columns=User.alt_user_df.columns)
                ], 
                ignore_index=True)

